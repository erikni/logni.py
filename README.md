# logni
Logging facility for Python

---

Example:

`# python`

`>>> from logni import log`

`>>> log.mask('ALL')` 

`>>> log.stderr(1)`

`>>> log.ni( 'Info message', INFO=3 )`
	
2015/07/15 15:16:01 [12274] I3: Info message [919a8785] {<stdin>:<module>():1} {'hash': '919a8785'}

`>>> log.ni( 'Error message', ERR=4 )`

2015/07/15 15:16:17 [12274] E4: Error message [d3238463] {<stdin>:<module>():1} {'hash': 'd3238463'}

`>>> log.ni( 'Debug message', DBG=1 )`

2015/07/15 15:16:35 [12274] D1: Debug message [b63ed3e0] {<stdin>:<module>():1} {'hash': 'b63ed3e0'}


