open-graph-card: \
_build/open-graph-card/final-assembly.png \
_build/open-graph-card/open-graph-card.svg \
_build/open-graph-card/open-graph-card.png


.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: lint
lint: lint-python lint-shell

.PHONY: lint-python lint-shell
lint-python lint-shell:
	./$@.sh

.PHONY: test
test:
	pytest

.PHONY: _build/open-graph-card/final-assembly.png
_build/open-graph-card/final-assembly.png:
	@mkdir -p $(@D)
	console export-png --width=640 --height=490 --no-label $@

_build/open-graph-card/open-graph-card.svg: _build/open-graph-card/final-assembly.png
	console open-graph-card > $@

_build/open-graph-card/open-graph-card.png: _build/open-graph-card/open-graph-card.svg
	cairosvg --unsafe $< -o $@
	optipng $@
	./image-meta.sh $@
