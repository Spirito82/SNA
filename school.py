import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

def printGraph(sequence):
	fig = plt.figure("Degree of a random graph", figsize=(20, 6))
	#sns.histplot(sequence, kde=True, stat='count', discrete=True)
	print(len(sequence))
	#print(sqrt(len(sequence)))
	p = sns.histplot(sequence, kde=True, stat='count', bins=len(set(sequence)))
	p.set_xlabel("Grades", fontsize=10)

	fig.tight_layout()
	plt.show()

def printCumulative(sequence):
	fig = plt.figure("Degree of a random graph", figsize=(20, 6))
	# sns.histplot(sequence, kde=True, stat='count', discrete=True)
	b = sns.ecdfplot(sequence)
	b.set_xlabel("Grades", fontsize=10)

	fig.tight_layout()
	plt.show()

def all_k_core(g, changed):
	for i in range(18, 36):
		core = nx.k_core(g, k=i)
		core_changed = nx.k_core(changed, k=i)

		print(str(i) + ": (" + str(len(core.nodes)) + ", " + str(len(core_changed.nodes)) + ")")

		print(core.nodes)
		print(core_changed.nodes)

		if len(core.nodes) != len(core_changed.nodes):
			print(core.nodes)
			print(core_changed.nodes)

def print_k_core(g, g_changed):
	k = nx.core_number(g)
	print({(k, v) for k, v in sorted(k.items(), key=lambda item: item[0])})
	core_number_before = {(k,v) for k, v in sorted(k.items(), key=lambda item: item[1])}

	k = nx.core_number(g_changed)
	print({(k, v) for k, v in sorted(k.items(), key=lambda item: item[0])})
	core_number_after = {(k,v) for k, v in sorted(k.items(), key=lambda item: item[1])}

	sequence_before = sorted((d for n, d in core_number_before))
	sequence_after = sorted((d for n, d in core_number_after))
	bin = len(set(sequence_before)) + 1
	plt.hist([sequence_before, sequence_after], bins=bin, label=["before", "after"])
	plt.xlabel('k-core')
	plt.ylabel('count')
	plt.show()

def print_centrality(g):
	degree_centrality = sorted(nx.degree(g), key=lambda item: item[1], reverse=False)
	degree_count = sorted(nx.degree(g, weight='count'), key=lambda item: item[1], reverse=False)
	degree_duration = sorted(nx.degree(g, weight='duration'), key=lambda item: item[1], reverse=False)
	print("first 25 percentile: " + str(degree_count[0:int(236 / 4)]))
	print("last 25 percentile: " + str(degree_count[int(3 * 236 / 4):236]))
	# printGraph(sorted((d for n, d in degree_centrality)))
	# printCumulative(sorted((d for n, d in degree_centrality)))
	# printGraph(sorted((d for n, d in degree_count)))
	# printCumulative(sorted((d for n, d in degree_count)))
	# printGraph(sorted((d for n, d in degree_duration)))
	# printCumulative(sorted((d for n, d in degree_duration)))
	print("asc degree: " + str(degree_centrality[0:10]))
	print("asc degree/count: " + str(degree_count[0:10]))
	print("asc degree/duration: " + str(degree_duration[0:10]))
	degree_centrality = sorted(nx.degree_centrality(g).items(), key=lambda item: item[1], reverse=True)
	degree_count = sorted(nx.degree(g, weight='count'), key=lambda item: item[1], reverse=True)
	degree_duration = sorted(nx.degree(g, weight='duration'), key=lambda item: item[1], reverse=True)
	print("desc degree: " + str(degree_centrality[0:10]))
	print("desc degree/count: " + str(degree_count[0:10]))
	print("desc degree/duration: " + str(degree_duration[0:10]))

def print_eigenvector_centrality(g):
	eigenvector_centrality = sorted(nx.eigenvector_centrality(g).items(), key=lambda item: item[1], reverse=True)
	eigenvector_count = sorted(nx.eigenvector_centrality(g, weight='count').items(), key=lambda item: item[1], reverse=True)
	print("desc eigenvector: " + str(eigenvector_centrality[0:10]))
	print("desc eigenvector/count: " + str(eigenvector_count[0:10]))

def print_betweenness_centrality(g):
	betweenness_centrality = sorted(nx.betweenness_centrality(g, k=236, seed=42, normalized=True, weight=None).items(),
									key=lambda item: item[1], reverse=True)
	print(betweenness_centrality)

def print_assortativity(g, g_changed):
	#r_count = nx.degree_assortativity_coefficient(g, weight='count')
	#r_duration = nx.degree_assortativity_coefficient(g, weight='duration')
	r = nx.degree_assortativity_coefficient(g)
	r_changed = nx.degree_assortativity_coefficient(g_changed)
	print("original assortativity coeffient: " + str(r))
	print("changed assortativity coeffient: " + str(r_changed))
	r_changed -= r
	print("changed-original assortativity " + str(r_changed))

# printCumulative(sorted((d for n, d in core_number)))
# printGraph(sorted((d for n, d in core_number)))

path = r".\sp_data_school\sp_data_school_day_1_g.gexf"
path_changed = r".\sp_data_school\sp_data_school_day_1_g - changed.gexf"
path_removed = r".\sp_data_school\sp_data_school_day_1_without_k-core=34.gexf"
path_big_changed = r".\sp_data_school\sp_data_school_day_1_g - big changed.gexf"

g = nx.read_gexf(path)
g_changed = nx.read_gexf(path_changed)
g_removed = nx.read_gexf(path_removed)
g_big_changed = nx.read_gexf(path_big_changed)

# CALCULATE K-CORE
print_k_core(g, g_changed)

# CALCULATE ALL K-CORE
all_k_core(g, g_changed)

# PRINT SINGLE CORE NODE LIST
core = nx.k_core(g, k=25)
core_changed = nx.k_core(g_changed, k=25)
print(core.nodes)
print(core_changed.nodes)

# ASSORTATIVITY INDEX
print_assortativity(g, g_changed)

# DEGREE CENTRALITY
print_centrality(g)

# EIGENVECTOR CENTRALITY
print_eigenvector_centrality(g_big_changed)

#BETWEEENNESS CENTRALITY
print_betweenness_centrality(g)

#ALL SHORTEST PATH FROM 1483 to 1761
#print([p for p in nx.all_shortest_paths(g, source='1483', target='1761')])
print([p for p in nx.all_shortest_paths(g, source='1483', target='1579')])
print([p for p in nx.all_shortest_paths(g, source='1753', target='1673')])
print([p for p in nx.all_shortest_paths(g, source='1441', target='1833')])
print([p for p in nx.all_shortest_paths(g, source='1521', target='1560')])
print([p for p in nx.all_shortest_paths(g, source='1913', target='1552')])
print([p for p in nx.all_shortest_paths(g, source='1465', target='1700')])
print([p for p in nx.all_shortest_paths(g, source='1805', target='1822')])
print([p for p in nx.all_shortest_paths(g, source='1609', target='1780')])
print([p for p in nx.all_shortest_paths(g, source='1710', target='1551')])
print([p for p in nx.all_shortest_paths(g, source='1917', target='1761')])