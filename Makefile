.PHONY: venv
venv:
	@pipenv shell

.PHONY: start-graphql
start-graphql:
	strawberry server main

.PHONY: start-fastapi
start-fastapi:
	@uvicorn main:app --reload

.PHONY: deta-deploy
deta-deploy:
	@deta deploy

.PHONY: bump-patch
bump-patch:
	@bump2version patch
	@git push --tags
	@git push

.PHONY: bump-minor
bump-minor:
	@bump2version minor
	@git push --tags
	@git push

.PHONY: bump-major
bump-major:
	@bump2version major
	@git push --tags
	@git push