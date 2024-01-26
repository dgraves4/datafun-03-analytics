'''This module provides a reusable byline for the author's business services and company analytics'''

import math
import statistics

#Define variables 
company_name: str = 'Analytics Maestro Inc.'
count_active_employees: int = 30
advanced_analytics_enabled: bool = True
average_revenue_per_user: float = 120.45
data_sources: list = ('Sales Database', 'Customer Survey', 'Web Analytics', 'Social Media')
project_revenue_amounts: list = (110.25, 130.65, 115.80, 125.10, 120.45)

#Define formatted strings
active_employees_string: str = f'Active Employees: {count_active_employees}'
advanced_analytics_string: str = f'Analytics Enabled: {advanced_analytics_enabled}'
revenue_per_user_string: str = f'Average Revenue Per User: {average_revenue_per_user}'
data_sources_string: str = f'Data Sources: {data_sources}'
project_revenue_string: str = f'Project Revenue: {project_revenue_amounts}'

#Descriptive Statistics
smallest = min(project_revenue_amounts)
largest = max(project_revenue_amounts)
total = sum(project_revenue_amounts)
count = len(project_revenue_amounts)
mean = statistics.mean(project_revenue_amounts)
mode = statistics.mode(project_revenue_amounts)
median = statistics.median(project_revenue_amounts)
standard_deviation = statistics.stdev(project_revenue_amounts)

#Stats String
stats_string: str = f'''
Descriptive Statistics for our Revenue values:
    Smallest: {smallest}
    Largest: {largest}
    Total: {total}
    Count: {count}
    Mean: {mean}
    Mode: {mode}
    Median: {median}
    Standard Deviation: {standard_deviation}'''

#Byline string defined
byline: str = f'''
{company_name}
{active_employees_string}
{advanced_analytics_string}
{revenue_per_user_string}
Data Sources: {', '.join(data_sources)}
Project Revenue: {', '.join(map(str, project_revenue_amounts))}'''
    
def main():
    '''Display all output'''
    print(byline) 
    print(stats_string)
    
if __name__ == '__main__':
    main()
