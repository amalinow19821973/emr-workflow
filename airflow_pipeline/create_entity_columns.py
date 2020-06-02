import pandas as pd
from workflow_read_and_write import standard_read_from_db, standard_write_to_db

def extract_entities(note):
    lines = note.split('\n')
    medications = []
    features = []

    for line in lines:
        words = line.split()
        word_index = 0
        while word_index < len(words):
            if '[' in words[word_index]:
                ent_end = word_index+1
                #take into account negation of an entity
                possible_negation = ''
                if words[word_index-1] == 'no' or words[word_index-1] == 'not':
                    possible_negation = words[word_index-1] + '_'
                if 'B-MEDICATION' in words[word_index]:
                    while ent_end < len(words) and 'I-MEDICATION' in words[ent_end]:
                        ent_end += 1
                    medication = possible_negation
                    for i,sub_ent in enumerate(words[word_index:ent_end]):
                        if i == 0:
                            medication += sub_ent.split('[')[0]
                        else:
                            medication += '_' + sub_ent.split('[')[0]
                    medications.append(medication)
                elif 'B-FEATURE' in words[word_index]:
                    while ent_end < len(words) and 'I-FEATURE' in words[ent_end]:
                        ent_end += 1
                    feature = possible_negation
                    for i,sub_ent in enumerate(words[word_index:ent_end]):
                        if i == 0:
                            feature += sub_ent.split('[')[0]
                        else:
                            feature += '_' + sub_ent.split('[')[0]
                    features.append(feature)
                word_index += ent_end
            else:
                word_index += 1

    return medications, features


def get_columns_from_notes(df):

    all_medication_entities = []
    all_general_feature_entities = []

    for i, row in df.iterrows():
        note = row['labeled_notes']
        medications, features = extract_entities(note)
        #remove duplicates from the list:
        medications = list(dict.fromkeys(medications))
        features = list(dict.fromkeys(features))
        #
        all_medication_entities.append(medications)
        all_general_feature_entities.append(features)

    df['medication_entities'] = all_medication_entities
    df['feature_entities'] = all_general_feature_entities

    return df
        

def create_entity_columns():
    df_json_encoded = standard_read_from_db('ner_labeled_notes')
    df = pd.read_json(df_json_encoded.decode())

    new_df = get_columns_from_notes(df)

    new_df_json_encoded = new_df.to_json().encode()
    standard_write_to_db('entity_columns', new_df_json_encoded)