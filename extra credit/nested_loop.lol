HAI
	I HAS A temp 
	I HAS A temp2
	I HAS A temp3

	BTW loop
	temp R 0
	IM IN YR loop UPPIN YR temp TIL BOTH SAEM 10 AN temp
		VISIBLE temp
	IM OUTTA YR loop 
	VISIBLE "------------------"

	BTW loop-loop-loop
	temp R 0
	IM IN YR loop UPPIN YR temp TIL BOTH SAEM 3 AN temp
		temp2 R 10
		IM IN YR inner_loop NERFIN YR temp2 TIL BOTH SAEM temp2 AN 5
			temp3 R 0
			IM IN YR third_loop UPPIN YR temp3 WILE DIFFRINT temp3 AN 5 
				VISIBLE "outer loop: " temp " inner loop: " temp2 " third loop: " temp3
			IM OUTTA YR third_loop
		IM OUTTA YR inner_loop
	IM OUTTA YR loop    
	VISIBLE "------------------"

	BTW loop-if then
	temp R 0
	temp2 R 5
	IM IN YR loop UPPIN YR temp TIL BOTH SAEM 10 AN temp
		BOTH SAEM temp AN temp2
		O RLY?
			YA RLY
				VISIBLE temp " == " temp2 ": stop loop"
				GTFO
			NO WAI
				VISIBLE temp " != " temp2 ": continue loop"
		OIC
	IM OUTTA YR loop 
	VISIBLE "------------------"

	BTW loop-switch case
	temp R 0
	IM IN YR loop UPPIN YR temp TIL BOTH SAEM 10 AN temp
		SUM OF 1 AN temp
		WTF?
		OMG 4
			VISIBLE "IT is 4"
			GTFO 
		OMG 6
			VISIBLE "IT is 6"
			GTFO
		OMGWTF
			VISIBLE "hello"
		OIC
	IM OUTTA YR loop

KTHXBYE