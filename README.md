# m2csv
This little program convert mysql output into csv file

## Requirement
* python 2.7

## Install
Clone this repository, then create an alias:        
```
alias m2csv='/path/to/m2csv/m2csv.py'
```

## Usage
### Synopsis
m2csv [-v] [-i INPUT FILE] [-o OUTPUT FILE]

	-v
		Verbose. Explain what happens.

	-i INPUT FILE
		Specify input file name, use STDIN if omitted.

	-o OUTPUT FILE
		Specify output file name, use STDOUT if omitted.

### Example
```
mysql -u u1 -p db1 -e 'select * from table1\G' | m2csv
```

```
mysql -u u1 -p db1 -e 'select * from table1\G' > result.txt
m2csv -i result.txt -o result.csv
```

## To-do list
* Support Unicode
* Support other mysql output formats
* Avoid overwriting output file
* Tested on python 2.7.6. Need to test on other version of python
