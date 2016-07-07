import cobra
import savvy
import pandas as pd

model=cobra.io.read_sbml_model('/Users/yanfenfu/Documents/local/cobra-5GB1/5GB1_ferm_EPS_complete.xml')
# change the methane uptake rate into 6.2, un-constrained
R_ch4_t=model.reactions.get_by_id("CH4tep") # select reaction using reaction name
R_ch4_t.lower_bound=6.2
R_ch4_t.upper_bound=6.2
sol=model.optimize()


# generate parameters for sobo analysis
input_var=savvy.sensitivity_tools.gen_params(2,('SGAT','EX_o2_e'),[(0,5),(-12,-9)],10,'/Users/yanfenfu/Documents/savvy',True)

print input_var
objFlux = list()
objFlux2=list()
control_rx = model.reactions.get_by_id('SGAT')
n=len(input_var)
for i in range(0, n):
    control_rx.lower_bound = input_var[i,0]
    control_rx.upper_bound = input_var[i,0]
    sol_controlled = model.optimize()
    objFlux.append(sol_controlled.f)
print objFlux
control_rx.lower_bound=-1000
control_rx.upper_bound=1000
control_rx=model.reactions.get_by_id('EX_o2_e')
for j in range(0, n):
    control_rx.lower_bound = input_var[j,1]
    control_rx.upper_bound = input_var[j,1]
    sol_controlled = model.optimize()
    objFlux2.append(sol_controlled.f)
print objFlux2
d=pd.DataFrame(objFlux)
d2=pd.DataFrame(objFlux2)
result = pd.concat([d, d2], axis=1)
print result
result.to_csv('test_result.csv', sep=',', encoding='utf-8')
savvy.sensitivity_tools.analyze_sensitivity('/Users/yanfenfu/Documents/savvy/saparams_2-parameters_10-n.txt','/Users/yanfenfu/Documents/local/cobra-5GB1/test_1.csv',1,',',1,'SGAT',True)