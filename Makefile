CODE_FOLDERS=src/ tests/

format:
	black ${CODE_FOLDERS}

check:
	black --check ${CODE_FOLDERS}
	mypy --install-types --non-interactive ${CODE_FOLDERS}
	pytest -v tests/