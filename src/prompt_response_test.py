from openai import OpenAI

class PatientSymptomDescr:

    def __init__(self):
        self.gender = 'female'
        self.age = 2
        self.weight = 33
        self.bmi = 22
        self.somatic_symptoms = []
        self.physical_exam_findings = []
        self.other_symptoms = []
    
    def add_somatic_symptom(self, symptom):
        if len(symptom) > 0:
            self.somatic_symptoms.append(symptom)
    
    def add_physical_exam_finding(self, physical_exam_findings):
        if len(physical_exam_findings) > 0:
           self.physical_exam_findings.append(physical_exam_findings)

    def add_other_symptoms(self, symptom):
        if len(symptom) > 0:
            self.other_symptoms.append(symptom)

    def make_prompt(self):
        s = f"""
        The patient is {self.age} year old {self.gender} who weights {self.weight} pounds with a BMI of {self.bmi}. 
        {self.get_symptoms_string()}
        """
        return s
    
    def make_item_list(self, lst):
        if len(lst) > 1:
            return ','.join(lst[:-1]) + ' and ' + lst[-1]
        else:
            return lst[-1]
    
    def get_symptoms_string(self):
        somatic = ('The patient\'s complaints include ' + self.make_item_list(self.somatic_symptoms)+'. ') if len(self.somatic_symptoms) > 0 else ''
        physical = ('Examining the patient, I found ' + self.make_item_list(self.physical_exam_findings) +'. ') if len(self.physical_exam_findings) > 0 else ''
        other = ('Other symptoms include ' + self.make_item_list(self.other_symptoms) +'. ') if len(self.other_symptoms) > 0 else ''
        return somatic + physical +  other 
    


def prompt_open_ai(prompt_str, model="gpt-3.5-turbo"):

    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
        {
        "role": "system",
        "content": """ I am taking care of a patient and would like your help generating a differential diagnosis.  I will provide details 
        about the patient and the symptoms below. Please output upto 5 conditions that are consistent with the symptoms sorted from the most likely to the least. Your 
        output must be in the format wherein each of the conditions must be in a separate line.
                        1. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>
                        2. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>
                        ...
                        5. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>
                        """
        },
        {
        "role": "user",
        "content": prompt_str
        }
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1
    )
    print(response)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def parse(msg): 
    """
    Go through each line of the message. It is of the form 
    1. <name of condition/disease>, <probability of this disease as a percentage>, <rationale as to why the patient may have this disease>
    2. <name of condition/disease>, <probability of this disease as a percentage>, <rationale as to why the patient may have this disease>
    ...
    5. <name of condition/disease>, <probability of this disease as a percentage>, <rationale as to why the patient may have this disease>
    Extract a list of [(<name of disease>, probability, <rationale>)]
    """
    lst_of_lines = msg.split('\n')
    result = []
    for (j, line) in enumerate(lst_of_lines):
        lst = line.split(',')
        if len(lst) >= 3:
            idx = int(lst[0][0])
            disease = lst[0][2:].strip()
            pct = lst[1].strip()[0:2]
            if pct[-1] =='%':
                pct = pct[:-1]
            rationale = lst[2].strip()
            print(f'{idx}. {disease}. {pct}%. {rationale}.')
            result.append((disease, pct, rationale))
    return result


def run_through_possibilities(n_trials=3):
    filename = 'output.csv'
    fhandle = open(filename, 'w')
    count = 0
    weakness_symptom = ['feeling weak', 'extreme weakness', 'being unable to lift objects', 'being unable to sit up']
    fatigue_symptom = ['reports being unable to play sports', 'feels fatigued', 'feels tired']
    physical_exam_rash = ['', 'rash', 'rash on face', 'rash on hands', 'rash on knuckles', 'rash on hands and face']
    confounder_symptoms = [[], ['frequent colds'], ['occasional fever'], ['pollen allergies'], ['frequent colds and fevers'] ]
    for w in weakness_symptom:
        for f in fatigue_symptom:
            for r in physical_exam_rash:
                for c_list in confounder_symptoms:
                    for c in c_list:
                        print(count)
                        p = PatientSymptomDescr()
                        p.add_somatic_symptom(w)
                        p.add_somatic_symptom(f)
                        p.add_physical_exam_finding(r)
                        p.add_other_symptoms(c)
                        print(p.make_prompt())
                        for j in range(n_trials):
                            resp = prompt_open_ai(p.make_prompt())
                            print(resp)
                            r_list = parse(resp)
                            print(r_list)
                            print(f'{count}, {j}, ', file=fhandle, end='')
                            print(f'{w}, {f}, {r}, \"{c_list}\",', file=fhandle, end='')
                            for (s, pct, rationale) in r_list:
                                print(f'{s}, {pct}, {rationale}, ', file=fhandle, end='')
                            print('', file=fhandle)
                            count = count + 1

    fhandle.close()

if __name__ == '__main__':
   # p = PatientSymptomDescr()
   # print(p.get_symptoms_string())
   # print(p.make_prompt())
   # resp = prompt_open_ai(p.make_prompt())
   # res = parse(resp)
   # print(res)
   run_through_possibilities()