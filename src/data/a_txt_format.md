# Text file data format


The name of the file is of the form `{target-disease}-{prompting modality}-{LLM-version}.txt` wherein the

  - `target-disease` is one of JDM (Juvenile Dermatomyositis), MCTD (Mixed Connective Dissue Disease), SLE (Lupus), SystemicSclerosis.
  - `prompting modality` can be formal or informal. Formal modality uses medical terminology for describing symptoms whereas the informal modality describes symptoms informally as a patient would.
  - `LLM-version` : we have tries chatgpt, claude and various versions.


Each file is a record of the patient symptoms and the parsed responses
in a machine readable format.

Here is an example for a particular patient.

The first line `P:` indicates a new patient record has begun  with the patient number, gender, age, height and weight.

Lines starting with `S:` record the symptoms that were generated.
Lines starting with `R:` record the responses.

The overall prompt for the LLM was symthesized using the `P:` and `S:`
lines. The LLM response was parsed to generate the `R:` lines.

~~~
P: 2, female, 10, 54, 46
S:Cannot stand up
S:Tired
S:Purple eyelids
S:Red cuticles 
S:Fever
S:Cold hands
S:Bumps under skin
R: 1, Juvenile Idiopathic Arthritis, 50,  the patient presents with joint pain, fatigue, fever, and bumps under the skin which are consistent with the symptoms of Juvenile Idiopathic Arthritis.
R: 2, Systemic Lupus Erythematosus, 20,  the patient's symptoms of fever, fatigue, purple eyelids, and bumps under the skin can be seen in Systemic Lupus Erythematosus.
R: 3, Juvenile Dermatomyositis, 15,  the patient's inability to stand up, fatigue, and purple eyelids are common in Juvenile Dermatomyositis which is an autoimmune condition affecting the muscles and skin.
R: 4, Kawasaki Disease, 10,  the combination of fever, red cuticles, and bumps under the skin can be indicative of Kawasaki Disease which is a condition that causes inflammation in the blood vessels.
R: 5, Sepsis, 5,  the patient's symptoms of fever, fatigue, and cold hands can be concerning for sepsis, especially if there is an underlying infection causing the symptoms.
~~~

