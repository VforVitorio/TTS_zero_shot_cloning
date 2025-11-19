IMAGE := tts-voice-cloning

build:
	docker build -t $(IMAGE) .

run-yourtts:
	docker run --rm \
		-e TEXT \
		-e PYTHONPATH=/opt/project \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/generate_yourtts.py

run-xtts:
	docker run --rm \
		-e TEXT \
		-e PYTHONPATH=/opt/project \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/generate_xtts.py

run-all:
	docker run --rm \
		-e TEXT \
		-e PYTHONPATH=/opt/project \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/run_all.py

jupyter:
	docker run -it --rm \
		-e PYTHONPATH=/opt/project \
		-p 8888:8888 \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

shell:
	docker run -it --rm \
		-e PYTHONPATH=/opt/project \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) /bin/bash

clean:
	docker rmi $(IMAGE)