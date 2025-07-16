.PHONY: reverse infect

reverse:
	@echo "Reversing the infection!"
	@./stockholm.py -r `cat example_key.txt`

infect:
	@echo "Infecting files!"
	@export STOCKHOLM_KEY=`cat example_key.txt` && ./stockholm.py
