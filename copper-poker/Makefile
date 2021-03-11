.PHONY : test build
test :
	@PYTHONPATH=copper-poker python -m pytest -p no:warnings --tb=auto -vv tests

single-test :
	@PYTHONPATH=copper-poker python -m pytest -p no:warnings --tb=auto -vv ${FILE}
