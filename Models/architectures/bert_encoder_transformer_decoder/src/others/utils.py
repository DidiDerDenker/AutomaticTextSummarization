# Imports
import os
import re
import shutil
import time

from others import pyrouge


# Global Variables
REMAP = {"-lrb-": "(", "-rrb-": ")", "-lcb-": "{", "-rcb-": "}", "-lsb-": "[", "-rsb-": "]", "``": '"', "''": '"'}


# Methods
def clean(x):
    return re.sub( r"-lrb-|-rrb-|-lcb-|-rcb-|-lsb-|-rsb-|``|''", lambda m: REMAP.get(m.group()), x)


def process(params):
    temp_dir, data = params
    hypotheses, references, pool_id = data
    cnt = len(hypotheses)
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    tmp_dir = os.path.join(temp_dir, "rouge-tmp-{}-{}".format(current_time, pool_id))

    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
        os.mkdir(tmp_dir + "/hypotheses")
        os.mkdir(tmp_dir + "/references")

    try:
        for i in range(cnt):
            if len(references[i]) < 1:
                continue

            with open(tmp_dir + "/hypotheses/cand.{}.txt".format(i), "w", encoding="utf-8") as f:
                f.write(hypotheses[i])

            with open(tmp_dir + "/references/ref.{}.txt".format(i), "w", encoding="utf-8") as f:
                f.write(references[i])

        r = pyrouge.Rouge155(temp_dir=temp_dir)
        r.model_dir = tmp_dir + "/references/"
        r.system_dir = tmp_dir + "/hypotheses/"
        r.model_filename_pattern = "ref.#ID#.txt"
        r.system_filename_pattern = r"cand.(\d+).txt"

        rouge_results = r.convert_and_evaluate()
        results_dict = r.output_to_dict(rouge_results)

    finally:
        pass

        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)

    return results_dict


def test_rouge(temp_dir, hyp, ref):
    hypotheses = [line.strip() for line in open(hyp, encoding="utf-8")]
    references = [line.strip() for line in open(ref, encoding="utf-8")]
    assert len(hypotheses) == len(references)

    cnt = len(hypotheses)
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    tmp_dir = os.path.join(temp_dir, "rouge-tmp-{}".format(current_time))

    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
        os.mkdir(tmp_dir + "/hypotheses")
        os.mkdir(tmp_dir + "/references")

    try:
        for i in range(cnt):
            if len(references[i]) < 1:
                continue

            with open(tmp_dir + "/hypotheses/hyp.{}.txt".format(i), "w", encoding="utf-8") as f:
                sentences = hypotheses[i].split("<q>")
                text = "\n".join(sentences)
                f.write(text)
                print(text) # TODO: Remove

            with open(tmp_dir + "/references/ref.{}.txt".format(i), "w", encoding="utf-8") as f:
                text = references[i]
                f.write(text)
                print(text) # TODO: Remove

        r = pyrouge.Rouge155(temp_dir=tmp_dir)
        r.model_dir = tmp_dir + "/references/"
        r.system_dir = tmp_dir + "/hypotheses/"
        r.model_filename_pattern = "ref.#ID#.txt"
        r.system_filename_pattern = r"hyp.(\d+).txt"
        scores = r.evaluate_rouge()

        # results_dict = r.output_to_dict(rouge_results)
        # print(rouge_results)

    finally:
        pass

        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)

    return scores


def tile(x, count, dim=0):
    """ Tiles x on dimension dim count times. """

    perm = list(range(len(x.size())))

    if dim != 0:
        perm[0], perm[dim] = perm[dim], perm[0]
        x = x.permute(perm).contiguous()

    out_size = list(x.size())
    out_size[0] *= count
    batch = x.size(0)

    x = x.view(batch, -1) \
         .transpose(0, 1) \
         .repeat(count, 1) \
         .transpose(0, 1) \
         .contiguous() \
         .view(*out_size)

    if dim != 0:
        x = x.permute(perm).contiguous()

    return x


def rouge_results_to_str(results_dict):
    return ">> ROUGE-F(1/2/3/l): {:.2f}/{:.2f}/{:.2f}/{:.2f}\nROUGE-R(1/2/3/l): {:.2f}/{:.2f}/{:.2f}/{:.2f}\n".format(
        results_dict["rouge_1_f_score"] * 100,
        results_dict["rouge_2_f_score"] * 100,
        results_dict["rouge_3_f_score"] * 100,
        results_dict["rouge_l_f_score"] * 100,
        results_dict["rouge_1_recall"] * 100,
        results_dict["rouge_2_recall"] * 100,
        results_dict["rouge_3_f_score"] * 100,
        results_dict["rouge_l_recall"] * 100
    )
