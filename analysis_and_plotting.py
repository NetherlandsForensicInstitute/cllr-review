import numpy as np
import pandas as pd
import pylab as pl
import seaborn as sns
import matplotlib.pyplot as plt
import textwrap
import scipy.stats as st
from matplotlib.cbook import boxplot_stats

# PLOT SAVE DIRECTORY
PLOT_SAVE_DIRECTORY = "Cllr Publication"

# Sent font globally
plt.rcParams.update({'font.family':'Times new Roman'})
plt.rcParams.update({'mathtext.default':  'regular' })

# Create year x-axis
years = [int(x) for x in np.linspace(2006, 2022, 17)]

# Read Literature data into dataframe
df = pd.read_excel('Data.xlsx')

# Create df with only automated systems
df_automated_systems = df[df['System Type'] == '(Semi)-Automated System']

# Create df with first occurrence of every title (also for automated systems and human experts)
df_unique_titles = df.groupby('Title').first().reset_index()

# Create seperate df with only automated systems
df_unique_titles_automated_systems = df_unique_titles[df_unique_titles['System Type'] == '(Semi)-Automated System']

# Group publications in areas with less than n values in "Other" group
values_treshold = 5
df_unique_titles_automated_systems['Forensic Area Publication Reduced'] = df_unique_titles_automated_systems['Forensic Area Publication']
values_per_area = df_unique_titles_automated_systems.groupby('Forensic Area Publication Reduced').filter(lambda x: x['Title'].count() < values_treshold).Title.array
df_unique_titles_automated_systems.loc[df_unique_titles_automated_systems['Title'].isin(values_per_area), 'Forensic Area Publication Reduced'] = 'Other'

# Print general interesting numbers
print("Number of publications on (semi-)automated LR systems:", len(df_unique_titles_automated_systems))
print("Number of publications on (semi-)automated LR systems that reported a Cllr:", len(df_unique_titles_automated_systems[df_unique_titles_automated_systems["Cllr Reported"] == "Yes"]))
print("Number of publications on (semi-)automated LR systems that reported a Cllr and a Cllr min:", len(df_unique_titles_automated_systems.dropna(subset=["Cllr min"])[df_unique_titles_automated_systems["Cllr Reported"] == "Yes"]))
print("Number of publications on (semi-)automated LR systems for which a Cllr could be calculated:", len(df_unique_titles_automated_systems[df_unique_titles_automated_systems["Search Category"] == "Cllr could be Calculated"]))
print("Number of Cllr values in all publications on (semi-)automated LR systems:", len(df_automated_systems['Cllr'].dropna()))
print("Number of Cllr values in all publications on (semi-)automated LR systems that were calculated:", len(df_automated_systems[df_automated_systems['Search Category'] == "Cllr could be Calculated"]['Cllr'].dropna()))
print("Number of forensically relevant Cllr values in all publications on (semi-)automated LR systems:", len(df_automated_systems[df_automated_systems["Taken into account for Range"] == "True"].dropna(subset=["Cllr"])))

# Create dataframe indicating per paper if the Cllr is reported or not
cllr_reported_automated_systems = pd.get_dummies(df_unique_titles_automated_systems['Cllr Reported'])
cllr_reported_automated_systems['Forensic Area'] = df_unique_titles_automated_systems['Forensic Area']
cllr_reported_automated_systems['Forensic Area Publication'] = df_unique_titles_automated_systems['Forensic Area Publication']
cllr_reported_automated_systems['Forensic Area Publication Reduced'] = df_unique_titles_automated_systems['Forensic Area Publication Reduced']
cllr_reported_automated_systems['Forensic Analysis'] = df_unique_titles_automated_systems['Forensic Analysis']
cllr_reported_automated_systems['Year'] = df_unique_titles_automated_systems['Year']
cllr_reported_automated_systems['Country'] = df_unique_titles_automated_systems['Country']

# Plot proportion of papers reporting Cllr per forensic area
CAT_VARIABLE = 'Forensic Area Publication Reduced'
ORDER_BY = df_unique_titles_automated_systems.replace(['Yes', 'No'], [1, 0]).groupby(CAT_VARIABLE).count().sort_values('Cllr Reported', ascending=False).index     # Order by bar heights
plt.figure(figsize=(18, 15))
sns.set_color_codes('muted')
ax1 = sns.barplot(df_unique_titles_automated_systems.groupby(CAT_VARIABLE).count(),
                  y=df_unique_titles_automated_systems.groupby(CAT_VARIABLE).count().index,
                  x='Authors',
                  color='white',
                  edgecolor="black", hatch=r"/",
                  label='All',
                  order=ORDER_BY,
                  zorder=3)
ax2 = sns.barplot(df_unique_titles_automated_systems[df_unique_titles_automated_systems['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count(),
                  y=df_unique_titles_automated_systems[df_unique_titles_automated_systems['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count().index,
                  x='Authors',
                  color="black",
                  label='Proportion Reporting $C_{llr}$',
                  order=ORDER_BY,
                  zorder=3)
proportions = [str(x) + '%' for x in (cllr_reported_automated_systems.groupby(CAT_VARIABLE).mean(numeric_only=True).reindex(ORDER_BY) * 100).round(1)["Yes"]]
ax1.bar_label(ax1.containers[0], labels=proportions, fontsize=40, padding=10)
sns.despine(left=True, bottom=True)
plt.legend(loc='lower right', fontsize=35)
# plt.title('Nr of Publications on (semi-)Automated LR Systems per Area', fontsize=40)
plt.ylabel("Forensic Area / Analysis", fontsize=40)
plt.xticks(fontsize=40)
labels = plt.gca().get_yticklabels()
# labels = [label.get_text() for label in labels]
labels[-1] = plt.text(0, 8.5, "Forensic Anthropology\n and Taphonomy")
plt.gca().set_yticklabels(labels, fontsize=38)
plt.xlabel('Number of Publications', fontsize=40)
plt.tight_layout()
plt.grid(axis='x', zorder=0)
plt.savefig(f"{PLOT_SAVE_DIRECTORY}/nr_of_publications_per_area.jpg", dpi=600)
plt.show()

# Plot proportion of papers reporting Cllr per year
CAT_VARIABLE = 'Year'
ORDER_BY = years    # Order by year
plt.figure(figsize=(15, 15))
sns.set_color_codes('muted')
ax1 = sns.barplot(df_unique_titles_automated_systems.groupby(CAT_VARIABLE).count(),
                  y=df_unique_titles_automated_systems.groupby(CAT_VARIABLE).count().index.astype(str),
                  x='Authors',
                  color='white',
                  edgecolor="black", hatch=r"/",
                  label='All',
                  order=ORDER_BY,
                  zorder=3)
ax2 = sns.barplot(df_unique_titles_automated_systems[df_unique_titles_automated_systems['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count(),
                  y=df_unique_titles_automated_systems[df_unique_titles_automated_systems['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count().index.astype(str),
                  x='Authors',
                  color="black",
                  label='Proportion Reporting $C_{llr}$',
                  order=ORDER_BY,
                  zorder=3)
proportions = [str(x) + '%' for x in (cllr_reported_automated_systems.groupby(CAT_VARIABLE).mean(numeric_only=True).reindex(ORDER_BY) * 100).round(1)["Yes"]]
proportions.pop(2)
ax1.bar_label(ax1.containers[0], labels=proportions, fontsize=33, padding=10)
sns.despine(left=True, bottom=True)
plt.legend(loc='upper right', fontsize=30)
# plt.title('Number of Publications on (semi-)Automated LR Systems per Year', fontsize=40, pad=20)
plt.yticks(fontsize=33)
plt.xticks(fontsize=30)
plt.xlabel('Number of Publications', fontsize=30)
plt.ylabel("Year", fontsize=30)
plt.xlim(right=18)
plt.tight_layout()
plt.grid(axis='x', zorder=0)
plt.savefig(f"{PLOT_SAVE_DIRECTORY}/nr_of_publications_per_year.jpg", dpi=600)
plt.show()

# Plot proportion of papers reporting Cllr per year (no DNA)
CAT_VARIABLE = 'Year'
ORDER_BY = years    # Order by year
df_unique_titles_as_no_dna = df_unique_titles_automated_systems[df_unique_titles_automated_systems['Forensic Analysis'] != 'DNA Analysis'] # Remove DNA Publications
cllr_reported_no_dna = cllr_reported_automated_systems[cllr_reported_automated_systems['Forensic Analysis'] != 'DNA Analysis']
plt.figure(figsize=(15, 15))
sns.set_color_codes('muted')
ax1 = sns.barplot(df_unique_titles_as_no_dna.groupby(CAT_VARIABLE).count(),
            y=df_unique_titles_as_no_dna.groupby(CAT_VARIABLE).count().index.astype(str),
            x='Authors',
            color='white',
            edgecolor="black", hatch=r"/",
            label='All',
            order=ORDER_BY,
            zorder=3)
ax2 = sns.barplot(df_unique_titles_as_no_dna[df_unique_titles_as_no_dna['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count(),
            y=df_unique_titles_as_no_dna[df_unique_titles_as_no_dna['Cllr Reported'] == 'Yes'].groupby(CAT_VARIABLE).count().index.astype(str),
            x='Authors',
            color="black",
            label='Proportion Reporting $C_{llr}$',
            order=ORDER_BY,
            zorder=3)
proportions = [str(x) + '%' for x in (cllr_reported_no_dna.groupby(CAT_VARIABLE).mean(numeric_only=True).reindex(ORDER_BY) * 100).round(1)["Yes"]]
proportions.pop(2)
ax1.bar_label(ax1.containers[0], labels=proportions, fontsize=33, padding=10)
sns.despine(left=True, bottom=True)
plt.legend(loc='upper right', fontsize=30)
# plt.title('Number of Publications on (semi-)Automated LR Systems per Year (No DNA)', fontsize=40)
plt.yticks(fontsize=33)
plt.xticks(fontsize=33)
plt.xlabel('Number of Publications', fontsize=30)
plt.ylabel("Year", fontsize=30)
plt.xlim(right=18)
plt.tight_layout()
plt.grid(axis='x', zorder=0)
plt.savefig(f"{PLOT_SAVE_DIRECTORY}/nr_of_publications_per_year_no_DNA.jpg", dpi=600)
plt.show()

# Stripplot of combination of Cllrs per forensic expertise area and in the area of forensic biometrics
df_taken_into_account_for_range = df_automated_systems[(df_automated_systems["Taken into account for Range"] == "True") & (df_automated_systems['Cllr Reported'] == 'Yes')]
df_relevant_cllrs = df_taken_into_account_for_range.loc[df_taken_into_account_for_range.groupby("Dataset")["Cllr"].idxmin()]
# Group publications in areas with less than n values in "Other" group
# values_treshold = 3
# df_relevant_cllrs['Forensic Area Publication Reduced'] = df_relevant_cllrs['Forensic Area Publication']
# values_per_area = df_relevant_cllrs.groupby('Forensic Area Publication Reduced').filter(lambda x: x['Dataset'].nunique() < values_treshold).Title.array
# df_relevant_cllrs.loc[df_relevant_cllrs['Title'].isin(values_per_area), 'Forensic Area Publication Reduced'] = 'Other'
plt.figure(figsize=(15, 15))
sns.set_color_codes('muted')
label_counts = df_relevant_cllrs.dropna(subset=['Cllr']).groupby('Forensic Area Publication').count().sort_values('Cllr', ascending=False)['Cllr']
cllr_count_order = label_counts.index
ax = sns.stripplot(df_relevant_cllrs.dropna(subset=['Cllr']), y='Forensic Area Publication', x='Cllr', order=cllr_count_order, color='black', s=8, zorder=3, jitter=0.25)
sns.despine(left=True, bottom=True)
# plt.title('$C_{llrs}$ per Forensic Area / Analysis', fontsize=35, pad=20)
plt.xticks(fontsize=30, rotation=0)
ax.set_yticklabels(labels=[f"{y} ({str(x)}) " for x,y in zip(label_counts, label_counts.index)])
plt.yticks(fontsize=30)
plt.xlim(0, 1.8)
plt.ylabel('Forensic Area / Analysis', fontsize=30)
plt.xlabel('$C_{llr}$', fontsize=30)
ax.grid(axis='x', zorder=0)
plt.tight_layout()
plt.savefig(f"{PLOT_SAVE_DIRECTORY}/cllr_distribution_per_area.jpg", dpi=600)
plt.show()
print(df_relevant_cllrs.groupby("Forensic Area Publication")['Cllr'].min())
print(df_relevant_cllrs.groupby("Forensic Area Publication")['Cllr'].max())