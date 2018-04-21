import csv
import pandas as pd
import os

os.chdir("\\\\phdi-storage01\\ProjectSpace\\WorkSpace\\3MStuff")

stateList = ["GA","PA","NY","SC","TN","TX","FL","MI","MS","MN","NC","AL","AR","AK","AZ","CA","CT","DE","HI","IA","IL","IN","KS","KY",
		     "LA","MA","MD","ME","MO","MT","ND","NE","NH","NJ","NM","NV","OH","OK","OR","RI","SD","UT","VA","VT","WA","WI","WV","WY"]
conditons = [("Upper Respiratory Infectons",["163"]),("Asthma",["138"]),("ADHD",["754"]),("Allergies",["105"]),("Major Mental Health",["775","776"]),("Acute Skin Diagnoses",["416"]),
("Acute Bronchitis and Bronchiolitis",["159"]),("Conduct and Behavior",["748"]),("Acute Respiratory Diagnoses - Moderate",["149"]),("Depression",["755","762"]),
("Depressive and Other Psychoses",["749"]),("Epilepsy and Epilepsy Complex",["14","24"]),("Dental Diagnoses",["110"]),("Acute Stress and Anxiety",["769"]),
("Chronic Mental Health",["751"]),("Chronic Stress",["757"]),("Psoriasis",["409","405"]),("Social Problems",["837","838","770"]),("Autism",["595"]),("Schizophrenia",["743"]),
("Diabetes2",["424"]),("BiPolar",["747"]),("Conjunctivitis and Eye Diagnoses",["94","88"]),("Developmental Language Disorder",["592"]),("Developmental Speech and Learning",["600"])]


def calc_cost(year, edcs, disease, minAge=0, maxAge=17):
	fin_list = [["State", "County", "Total Cost", "Number of Children"]]
	for st in stateList:
		print(st, year, disease)
		try:
			patient_df = pd.read_csv(st+year+"\\edc"+st+year+".csv")
			patient_df['patient_id'] = patient_df['PatientID']
			patient_df = patient_df[(patient_df['Age'].astype(int) >= minAge)
									 & (patient_df['Age'].astype(int) <= maxAge)
									 & (patient_df['EDCs'] != '')
									 & (patient_df['Months'].astype(int) > 0)]

			cost_df = pd.read_csv(st+year+"\\byPatient"+st+year+".csv")
			cost_df = cost_df[['patient_id', 'Cost']]

			patient_df = patient_df.merge(cost_df, how='left')

			def edcs_per_disease(row):
				total_diseases = len(str(row['EDCs']).strip().split(' '))
				return (float(row['Cost']) / total_diseases) / (12.0 / row['Months'])
			patient_df['cost_per_disease'] = patient_df.apply(edcs_per_disease, axis=1)

			for county, data in patient_df.groupby('County'):
				temp_total_cost = 0
				for index, row in data.iterrows():
					for dis in edcs:
						if dis in str(row['EDCs']).strip().split(' '):
							temp_total_cost += row['cost_per_disease']
				fin_list.append([st, str(county), temp_total_cost, len(data)])
		except:
			continue

	f = open('\\\\phdi-storage01\\ProjectSpace\\WorkSpace\\AlexMoran\\Data Visualization\\20{0}\\{1}_cost.csv'.format(year, disease), "w", newline = "")
	writer = csv.writer(f)
	writer.writerows(fin_list)
	f.close()	


def remove_less_than_11(year, disease):
	df = pd.read_csv('\\\\phdi-storage01\\ProjectSpace\\WorkSpace\\AlexMoran\\Data Visualization\\20{0}\\{1}_cost.csv'.format(year, disease))
	df['Number of Children'] = [0 if i < 11 else i for i in df['Number of Children']]

	def convert_cost_to_0(row):
		if row['Number of Children'] == 0:
			return 0
		else:
			return row['Total Cost']
	df['Total Cost'] = df.apply(convert_cost_to_0, axis=1)
	df.to_csv('\\\\phdi-storage01\\ProjectSpace\\WorkSpace\\AlexMoran\\Data Visualization\\20{0}\\{1}_cost_cleaned.csv'.format(year, disease), index=False)


for cond in conditons:
	for year in ['11', '12']:
		calc_cost(year, cond[1], cond[0])
		remove_less_than_11(year, cond[0])

