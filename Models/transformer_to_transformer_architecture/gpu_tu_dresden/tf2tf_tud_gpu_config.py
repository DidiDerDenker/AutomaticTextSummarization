language = "german"
model_name = "bert-base-multilingual-cased"
tokenizer_name = "bert-base-multilingual-cased"
batch_size = 16

ratio_corpus_wiki = 1.00
ratio_corpus_news = 1.00
ratio_corpus_mlsum = 1.00

path_output = "/scratch/ws/1/davo557d-ws_project/"
path_checkpoint = "/scratch/ws/1/davo557d-ws_project/checkpoint-50000"

text_english = """Almost as soon as the World Trade Center's Twin Towers fell on September 11, 2001, thousands of firefighters, police officers, construction workers, search-and-rescue dogs and volunteers headed to Ground Zero to look for survivors. Because they didn’t know how many people were trapped alive in the wreckage, firefighters and other rescue workers had to search carefully through the unstable piles of rubble for air pockets, called \"voids\", where they might find people who had been unable to escape from the collapsing buildings. To be safe, they didn’t use any heavy equipment at first. Some dug with their bare hands, while others formed bucket brigades to move small amounts of debris as efficiently as possible. Unfortunately, there were not many survivors to find: Two firemen were pulled from their truck in a cavity beneath some wreckage, and a few people were pinned at the edges of the pile. By September 12, workers had rescued all of the people who were trapped at the site. After that, the Ground Zero workers had a new and more heartbreaking mission: to sift carefully through the debris in search of human remains. The fallen buildings were unstable, and engineers worried that the weight of trucks and cranes would cause the wreckage to shift and collapse again, so the workers had to keep using the bucket brigades. Meanwhile, huge fires continued to burn at the center of the pile. Jagged, sharp pieces of iron and steel were everywhere. The work was so dangerous that many firefighters and police officers wrote their names and phone numbers on their forearms in case they fell into the hole or were crushed."""
text_german = """Der 11. September 2001 war ein schöner Spätsommertag in New York – bis um 08:46 Uhr ein Flugzeug in den Nordturm des World Trade Centers flog. Zunächst ging man von einem tragischen Unfall aus. Dann aber flog eine 2. Boeing in den Südturm. Die Bilder, die an diesem Tag und an den folgenden Jahrestagen um die Welt gingen, machen noch heute sprach- und fassungslos. Für mehr als 2.500 Menschen wurden die brennenden Hochhaustürme zur Todesfalle; fast 400 Feuerwehrleute und Polizeibeamte verloren bei den Rettungsarbeiten ihr Leben. Dieser traurige Tag ging fortan als '9/11' in die Geschichte ein. New York stand nach dem Anschlag auf das World Trade Center verständlicherweise unter Schock und vor einem Desaster unglaublichen Ausmaßes. Die Trümmer qualmten noch bis in den Dezember 2001 hinein und es sollte rund 9 Monate dauern, bis die insgesamt 1,8 Mio. Tonnen Schutt weggeräumt waren. Seither klafft an der Stelle, wo zuvor die 'Twin Tower' standen, eine riesige Wunde in Manhattans Stadtbild. Nach den Aufräumarbeiten auf dem World Trade Center Gelände blieb eine riesige Grube zurück: Ground Zero. Am Zaun sind die Ereignisse des 11. September dokumentiert. Seit 2011 gibt es einen Gedenkpavillon, in 2012 wurde das 'National September 11 Memorial and Museum' eröffnet."""

'''
- bert-base-multilingual-cased
- deepset/gbert-base
- xlm-roberta-base
- facebook/mbart-large-50
'''
