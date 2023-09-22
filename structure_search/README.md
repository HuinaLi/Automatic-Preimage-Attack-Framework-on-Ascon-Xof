Contents of the files:

code files:
1. ascon_optimal_ls.py: the code to describe model initialization and  generate initial state CNF.

2. get_cons_cnf_ascon.py: the code to generate all contraints in CNF form.

3. get_allcons_cnf_ascon.py: the code to generate all contraints of n rounds in CNF form.

4. combine_cons_inv_cnf.py: the code to combine n-round structure model's CNF including: 
1). Initial state CNFs (generete using ascon_optimal_ls.py), 
2). All constraints CNFs (using get_allcons_cnf_ascon.py), 

5. combine_object_cnf_ascon.py: the code to generate the final n-round structure search SAT model by combining Initial state's CNFs and All constraints' CNFs, as well as Objective funcition's CNFs.

6. read_and_ban_solution_ascon.py: the code to solve our model, we incorporate the concept of rotational symmetry here, in this way, the solver will exclude rotationally-equivalent solutions and continue searching for new ones that are distinct.

7. combine_and_solve_ascon.sh: the code to help me automatically return all solutions with detailed search time.


result folder:
1. all_2r_quadratic_structures_de_27.log: the result to print all feasiable quadratic structures with de = df =27.

1. all_3r_quartic_structures_de_6.log: the result to print all feasiable quartic structures with de = df = 6.
