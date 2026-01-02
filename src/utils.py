import random 
import pandas as pd
from openai import OpenAI


class Symptom:
    def __init__(self, name, pct, informal_descriptions):
        self.name = name
        self.pct = pct 
        self.informal = informal_descriptions
        
    def get_informal_symptom(self):
        if len(self.informal) <= 0 :
            return self.name
        else:
            return random.choice(self.informal)
        
def make_prompt(symptom_list, gender, age, weight, height):
    patient_descr = f'The patient is a {age} year old {gender} with a weight of {weight} lbs and height of {height} inches.'
    symptoms_str = 'The list of symptoms include '
    for (j, s) in enumerate(symptom_list):
        if j != len(symptom_list)-1:
            symptoms_str = symptoms_str + f' ({j+1}) {s}'
        else:
            symptoms_str = symptoms_str + f' and ({j+1}) {s}.'
    return patient_descr + ' ' + symptoms_str

def prompt_open_ai(prompt_str, model="gpt-3.5-turbo", debug=False):
    client = OpenAI()
    if debug:
        print(f'Model: {model}')
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
    #print(response)
    #print(response.choices[0].message.content)
    if debug:
        print(response)
    return response.choices[0].message.content

import re
def parse_response(response):
    lst_of_lines = response.split('\n')
    results = []
    for (j, line) in enumerate(lst_of_lines): 
        m = re.match(r"(\d+).\s*(.*)\s*,\s*(\d+)%,(.*)", line)
        if m != None:
            results.append((m.group(2), m.group(3), m.group(4)))
    return results

def run_symptoms_list_openai_and_parse_responses(symptoms_list_list, gender, age, weight, height, max_n=None, model="gpt-3.5-turbo"):
    count = 0
    all_parsed_responses = []
    for symptoms_list in symptoms_list_list:
        p0 = make_prompt(symptoms_list, gender, age, weight, height)
        r0 = prompt_open_ai(p0, model)
        parsed_r0 = parse_response(r0)
        all_parsed_responses.append(parsed_r0)
        count = count + 1
        if max_n != None and count >= max_n:
            return all_parsed_responses
    return all_parsed_responses

def dump_responses_to_file(symptoms_list_list, all_parsed_responses, filename, gender, age, weight, height):
    filehandle = open(filename, 'w')
    count = 0
    for (symptoms_list, parsed_response) in zip(symptoms_list_list, all_parsed_responses):
        count = count + 1
        print(f'P: {count}, {gender}, {age}, {weight}, {height}', file=filehandle)
        for s in symptoms_list:
            print(f'S:{s}', file=filehandle)
        for (j, r) in enumerate(parsed_response):
            (disease_name, prob, descr) = r
            print(f'R: {j+1}, {disease_name}, {prob}, {descr}', file=filehandle)
    filehandle.close()

def dump_responses_to_file(symptoms_list_list, all_parsed_responses, filename, gender, age, weight, height):
    filehandle = open(filename, 'w')
    count = 0
    for (symptoms_list, parsed_response) in zip(symptoms_list_list, all_parsed_responses):
        count = count + 1
        print(f'P: {count}, {gender}, {age}, {weight}, {height}', file=filehandle)
        for s in symptoms_list:
            print(f'S:{s}', file=filehandle)
        for (j, r) in enumerate(parsed_response):
            (disease_name, prob, descr) = r
            print(f'R: {j+1}, {disease_name}, {prob}, {descr}', file=filehandle)
    filehandle.close()

import anthropic


anthropic_client = anthropic.Anthropic(
    api_key="...",
)

def prompt_anthropic(prompt_str, model='claude-3-sonnet-20240229'):
    message = anthropic_client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=0,
        system="I am taking care of a patient and would like your help generating a differential diagnosis.  I will provide details \n        about the patient and the symptoms below. Please output upto 5 conditions that are consistent with the symptoms sorted from the most likely to the least. Your \n        output must be in the format wherein each of the conditions must be in a separate line.\n                        1. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>\n                        2. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>\n                        ...\n                        5. <name of condition/disease>, <probability of this disease as a percentage>, <brief rationale as to why the patient may have this disease>",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{prompt_str}"
                    }
                ]
            }
        ]
    )
    return message.content[0].text 

def run_symptoms_list_anthropic_and_parse_responses(symptoms_list_list, gender, age, weight, height, max_n=None, model='claude-3-sonnet-20240229'):
    count = 0
    all_parsed_responses = []
    for symptoms_list in symptoms_list_list:
        p0 = make_prompt(symptoms_list, gender, age, weight, height)
        r0 = prompt_anthropic(p0)
        parsed_r0 = parse_response(r0)
        all_parsed_responses.append(parsed_r0)
        count = count + 1
        if max_n != None and count >= max_n:
            return all_parsed_responses
    return all_parsed_responses

def run_symptoms_list_and_parse_responses(symptoms_list_list, gender, age, weight, height, max_n=None, model='gpt-3.5-turbo'):
    if 'gpt' in model: 
        return run_symptoms_list_openai_and_parse_responses(symptoms_list_list, gender, age, weight, height, max_n = max_n, model=model)
    else:
        return run_symptoms_list_anthropic_and_parse_responses(symptoms_list_list, gender, age, weight, height, max_n, model)

# select all cases where JDM is not the top response.
def approx_matches(keywords_lst, symp_lst):
        # check if any string in the list has symp as a substring
        return any([s.lower() in symp.lower() for s in keywords_lst for symp in symp_lst])

def select_where_x_is_not_top(all_patients, resp_list):
    return [p for p in all_patients if not approx_matches(resp_list, p.get_top_three_symptoms())]


class PatientData:
    def __init__(self, number, gender, age, weight, height):
        self.n = number
        self.gender = gender
        self.age = age
        self.weight=weight
        self.height=height 
        self.symptom_list = []
        self.responses = {}
        
    def add_symptom(self, s):
        self.symptom_list.append(s)
        
    def add_response(self, resp_id, diag, pct, reasoning):
        assert resp_id not in self.responses
        self.responses[resp_id] = (diag, pct, reasoning)
        
    def get_top_symptom(self):
        if 1 not in self.responses:
            return None
        return self.responses[1][0]
    
    def get_top_three_symptoms(self, k = 3):
        lst = [v[0] for (i, v) in self.responses.items() if i <= k]
        return lst
    
def process_file(filename, debug=False):
    file = open(filename,'r')
    cur_patient = None
    all_patients = []
    for line in file:
        m = re.match('\s*P:\s*(\d+\.?\d*),\s*(male|female)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*,\s*(\d+\.?\d*)\s*', line)
        if m:
            if debug:
                print(f'Patient: number {m.group(1)}, gender {m.group(2)}, age {m.group(3)}, weight {m.group(4)}, height {m.group(5)}')
            if cur_patient != None:
                all_patients.append(cur_patient)
            cur_patient = PatientData(int(m.group(1)), m.group(2), int(m.group(3)), float(m.group(4)), float(m.group(5)))
        else:
            m = re.match('s*S:\s*(.*)', line)
            if m:
                if debug:
                    print(f'Symptom: {m.group(1)}')
                assert cur_patient != None
                cur_patient.add_symptom(m.group(1))
            else:
                m = re.match('\s*R:\s*(\d+)\s*,\s*(.*)\s*,\s*(\d+)\s*,\s*(.*)', line)
                if m:
                    resp_id = int(m.group(1))
                    diag = m.group(2).strip()
                    pct = int(m.group(3))
                    reasoning = m.group(4).strip()
                    if debug:
                        print(f'response: {resp_id},*{diag}*,{pct}%,*{reasoning}*')
                    assert cur_patient != None
                    cur_patient.add_response(resp_id, diag, pct, reasoning)
    return all_patients


def mk_prompt(pat):
    return make_prompt(pat.symptom_list, pat.gender, pat.age, pat.weight, pat.height)

def run_llm_and_parse_response(pat, model):
    print(f'Patient ID: {pat.n}')
    prompt = mk_prompt(pat)
    if 'gpt' in model:
        r = prompt_open_ai(prompt, model)
    else: 
        r = prompt_anthropic(prompt, model)
    return parse_response(r)

