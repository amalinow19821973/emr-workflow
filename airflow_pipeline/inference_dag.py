from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

import get_new_records_for_predictions
import new_records_ner_prep_clean_notes
import new_records_make_ner_input_file
import new_records_inference_per_100000
import new_records_add_labeled_notes_column
import new_records_create_entity_columns
import new_records_lda_topics_per_note

default_args = {
    'owner': 'EMR Appliance Pipeline',
    'start_date': datetime(2020,1,24)
}

dag = DAG('emr-inference-dag', default_args=default_args)

new_records_operator = PythonOperator(
    task_id = 'get_new_records',
    python_callable=get_new_records_for_predictions.get_records,
    dag = dag
    )

ner_clean_notes_operator = PythonOperator(
    task_id = 'ner_clean_notes',
    python_callable = new_records_ner_prep_clean_notes.clean_ner_notes,
    dag = dag
    )

ner_input_file_operator = PythonOperator(
    task_id = 'ner_make_input_file',
    python_callable = new_records_make_ner_input_file.create_file,
    dag = dag
    )

ner_label_notes_operator = PythonOperator(
    task_id = 'ner_label_notes',
    python_callable = new_records_inference_per_100000.label_notes,
    dag = dag
    )

ner_labeled_notes_column_operator = PythonOperator(
    task_id = 'ner_add_labeled_notes_column',
    python_callable = new_records_add_labeled_notes_column.create_labeled_notes_column,
    dag = dag
    )

ner_entity_column_operator = PythonOperator(
    task_id = 'ner_add_entity_columns',
    python_callable = new_records_create_entity_columns.create_entity_columns,
    dag = dag
    )

lda_topics_operator = PythonOperator(
    task_id = 'lda_topics_per_note',
    python_callable = new_records_lda_topics_per_note.get_ngrams_per_note,
    dag = dag
    )

new_records_operator.set_downstream([ner_clean_notes_operator, lda_topics_operator])

ner_clean_notes_operator.set_downstream(ner_input_file_operator)
ner_input_file_operator.set_downstream(ner_label_notes_operator)
ner_label_notes_operator.set_downstream(ner_labeled_notes_column_operator)
ner_labeled_notes_column_operator.set_downstream(ner_entity_column_operator)
