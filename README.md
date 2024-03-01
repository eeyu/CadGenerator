# CadGenerator

## Scad to Onshape
The following converts an scad file to a Brep format in onshape
### Quickstart

1. Create and load a new conda environment. Python v3.8+ works
2. pip install -r requirements.txt
3. For a quick demo, cd into CadGenerator/ and run 
```
python -m PartGenerator.scad_conversion_main --mode example --example 148
```
The available examples are 011, 096, 107, 114, 128, 162

The output is located by default at this [part studio](https://cad.onshape.com/documents/c3b4576ef97b70b3e09ba2f0/w/2a155a6e88e3a953e49858f7/e/2a5362fe0e6cb33b327a98de)

You can send custom scad files by running 
```
python -m PartGenerator.scad_conversion_main --mode custom --example PartGenerator/scad/your_scad.scad
```

### Notes 
This code primarily demonstrates the pipeline. It can only convert scad build from simple operations like primitives, 
booleans, and transforms. It was meant to interface with the output of the [InverseCSG paper](https://github.com/yijiangh/InverseCSG)
