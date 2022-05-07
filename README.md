# Truss solver

A CLI program to solve truss problems. The first time you run the program,
it'll ask you about how many nodes your truss have and to name all of the forces
that are unknown to you. Then, the program will ask you about the expression that
describes the sum of all forces in the horizontal and the vertical direction for
each node.

## Rules to fill in the CLI

Because the output of the CLI input is just a string, there are some rules to be
obey in this step.

1. The force names are separated by commas and are space insensitive;
2. The expressions are separated by plus signals and are space insensitive only
   between the signals;
3. Negative signs are attatched to the expression;
4. You need to obey the names you selected for each force;
5. To multiply the forces by a scalar, follow these formats:
   - force\*scalar to multiply by a scalar;
   - force\*num/denom to multiply by a fraction;
   - force\*sinX or force\*cosX, with X being any angle in degrees.
6. Special rules include:
   - You don't need to specify when the scalar is one;
   - Any number will be summed up;
   - Any force left over becomes zero.

## After run

After you run the file for the first time, it'll generate a json file that you can
reuse to run the program. This way, you can make minor changes without having to
type everything again. To run the program again using the file, just specify the
name of the file after the program when you run it.

```
$ python truss_solver.py output.json
```
