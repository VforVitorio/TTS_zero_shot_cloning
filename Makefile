IMAGE := tts-voice-cloning

build:
	docker build -t $(IMAGE) .

run-coqui:
	docker run --rm \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/generate_coqui.py

run-gptsovits:
	docker run --rm \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/generate_gptsovits.py

run-all:
	docker run --rm \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) python scripts/run_all.py

jupyter:
	docker run -it --rm \
		-p 8888:8888 \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

shell:
	docker run -it --rm \
		-v "$(PWD):/opt/project" \
		-w /opt/project \
		$(IMAGE) /bin/bash

clean:
	docker rmi $(IMAGE)