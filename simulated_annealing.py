#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as etree
import random

tree = etree.parse('9x800x50.jobs')
root = tree.getroot()
all_links = tree.findall('.//REQUEST')
max_computer = 20

def generate_list_config(variable_arrival_time):
	list_nodes_time = []
	start_count = 0
	count_end = 0
	for options_task in root:
		list_config = []
		count_end += int(options_task.attrib['COUNTREQUESTS'])
		if int(options_task.attrib['ARRIVALTIME']) == variable_arrival_time:
			for i in range(start_count, count_end):
				list_nodes_time.append(all_links[i].attrib['NODES'])
				list_nodes_time.append(all_links[i].attrib['TIME'])
				list_config.append(list_nodes_time)
				list_nodes_time = []
			return list_config
		start_count = count_end

def generate_work_dict(input_dict, list_pass):

	variable_options = []
	output_config = []
	number_task = []
	for i in input_dict:
		if (i in list_pass) == 0:
			number_task.append(i)
			variable_options = input_dict[i]
			choise = random.randint(1, len(variable_options))
			output_config.append(variable_options[choise - 1])

	return number_task, output_config

def container_data(Task, index, bias, start):

	test_list = []
	for i in range(1 + bias, (int(Task[0]) + 1) + bias):
		test_list.append(i)
	param_task = [index, start, int(Task[1]) + start, test_list]

	return param_task

def parameter_container(Task, index):

	list_data = []
	param_task = container_data(Task, index, 0, 0)
	list_data.append(param_task)
	container = {
		'container_index' : index,
		'V_container' : max_computer * int(Task[1]),
		'V_left' : max_computer * int(Task[1]) - int(Task[0]) * int(Task[1]),
		'computer_count' : max_computer,
		'time_max' : int(Task[1]),
		'container_data' : list_data
	}

	return container

def add_new_container(index, work, list_container, max_v_left_in_container):

	container = parameter_container(work, index)
	list_container.append(container)
	if container['V_left'] >= max_v_left_in_container:
		max_v_left_in_container = container['V_left']

	return container, list_container, max_v_left_in_container

def record_func(container_add, Task_add, index, start, bias):

	test_list = container_data(Task_add, index, bias, start)
	list_cont = container_add['container_data']
	list_cont.append(test_list)
	container_add['container_data'] = list_cont
	container_add['V_left'] = container_add['V_left'] - int(Task_add[0]) * int(Task_add[1])

	return container_add

def add_data_container(container_add, Task_add, index):

	for i in range(len(container_add['container_data'])): 
		work_list = container_add['container_data'][i]
		if int(Task_add[1]) >= int(container_add['time_max'] - work_list[2]) and i == len(container_add['container_data']) - 1:
			bias = work_list[3][len(work_list[3]) - 1]
			if bias + int(Task_add[0]) <= container_add['computer_count'] and container_add['time_max'] >= int(Task_add[1]):
				start = 0
				container_add = record_func(container_add, Task_add, index, start, bias)
			else:
				return "ERROR"

		if work_list[1] == 0:
			max_nod = len(work_list[3])

		if int(container_add['time_max'] - work_list[2]) >= int(Task_add[1]) and i == len(container_add['container_data']) - 1:
			if container_add['V_left'] - int(Task_add[0]) * int(Task_add[1]) >= 0 and int(Task_add[0]) <= max_nod and container_add['time_max'] >= int(Task_add[1]):
				bias = work_list[3][0] - 1
				if bias + int(Task_add[0]) <= container_add['computer_count']:
					start = int(work_list[2])
					container_add = record_func(container_add, Task_add, index, start, bias)
				else:
					return "ERROR"
			else:
				bias = work_list[3][len(work_list[3]) - 1]
				if bias + int(Task_add[0]) <= container_add['computer_count'] and container_add['time_max'] >= int(Task_add[1]):
					start = 0
					container_add = record_func(container_add, Task_add, index, start, bias)
				else:
					return "ERROR"

	return container_add

def Best_Fit_Decreasing_High():

	container_count = 0; list_container = []; list_min_left = []; list_time_cont = []
	for i in work_dict:				
		if container_count == 0:
			container_count += 1
			container = parameter_container(work_dict[i], i)
			list_container.append(container)
			max_v_left_in_container = container['V_left']
			one_task = work_dict[i]

		add_task = work_dict[i]
		count_p = 0
		for contain in list_container:
			list_min_left.append(contain['V_left'] - int(add_task[0]) * int(add_task[1]))

		count_zero = 0
		list_min = []
		for left in list_min_left:
			if left <= 0:	
				count_zero += 1
			else:
				list_min.append(left)

			if count_zero == len(list_min_left) and work_dict[i] != one_task:
				container_count += 1
				container, list_container, max_v_left_in_container = add_new_container(i, work_dict[i], list_container, max_v_left_in_container)
				break

		list_min.sort()
		count_error = 0
		for contain in list_container:
			for min_c in list_min:
				if contain['V_left'] - int(add_task[0]) * int(add_task[1]) == min_c and work_dict[i] != one_task:
					container = add_data_container(contain, add_task, i)
					if container == "ERROR":
						count_error += 1
						break
					else:
						list_min = []
						break
					break

			if count_error == len(list_min) and count_error != 0 and work_dict[i] != one_task:
				container_count += 1
				container, list_container, max_v_left_in_container = add_new_container(i, work_dict[i], list_container, max_v_left_in_container)
				count_error = 0
				continue

		list_min_left = []

	return list_container


dict_jobs = {}; work_dict = {}; list_pass = []; best_s = []; best_cont = []; left_cont = []; best_cont1 = []
dict_jobs = { arrival_time : generate_list_config(arrival_time) for arrival_time in range(1, len(root) + 1) }

T = 300; T_min = 2; count_t = 0; best_cel = 0
T_0 = T

while T >= T_min:

	number_task, output_config = generate_work_dict(dict_jobs, list_pass)
	work_dict = { number_task[i] : output_config[i] for i in range(len(output_config)) }
	list_container = Best_Fit_Decreasing_High()
	proc = 0; rez = 0; count = 0; rez1 = 0; data_len1 = 0; count_con = []

	for cont in list_container:
		proc = int(cont['V_left']) / (int(cont['V_container']) / 100.0)
		data_len1 += len(cont['container_data'])
		if proc <= 1:
			rez += len(cont['container_data'])
			for best_container_data in cont['container_data']:
				list_pass.append(best_container_data[0])
			count += 1
			best_cont.append(cont)
		else:
			count_con.append(proc)
			rez1 += len(cont['container_data'])
			left_cont.append(cont)

	best_cont1.extend(best_cont)
	best_cont1.extend(left_cont)
	cel_t = 0
	P = random.randint(1, 200)

	for c_f in best_cont1:
		cel_t += c_f['time_max']

	if best_cel == 0:
		best_cel = cel_t
		print 'start_s', cel_t
		print '===================================='

	if cel_t <= best_cel:
		best_cel = cel_t
		best_s = []
		best_s.extend(best_cont)
		best_s.extend(left_cont)
		print '--------------------->', count, rez, len(best_s), rez1, data_len1, cel_t

	elif P == 47:	
		T += 50
		best_cel = cel_t
		best_s = []
		best_s.extend(best_cont)
		best_s.extend(left_cont)
		print 'Bad------------------>', count, rez, len(best_s), rez1, data_len1, cel_t

	T = T_0 / (1 + count_t)
	count_t += 1
	best_cont1 = []
	left_cont = []

cel = 0; count = 0; proc = 0
print '===================================='

for i in best_s:
	cel += i['time_max']
	proc = int(i['V_left']) / (int(i['V_container']) / 100.0)	
	if proc <= 1:
		count += 1

print 'best_s', cel

#print count_con
