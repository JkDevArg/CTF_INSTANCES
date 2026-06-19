SHELL := /bin/bash
.DEFAULT_GOAL := help
.PHONY: help check-deps all lab01 lab02 lab03 lab04 stop clean status

help:
	@printf "\n\033[1;36m  ╔══════════════════════════════════════════════╗\n"
	@printf "  ║   Ethical Hacking Lab Suite  v4.0            ║\n"
	@printf "  ╠══════════════════════════════════════════════╣\n"
	@printf "  ║\033[0m  make check-deps   Verificar dependencias    \033[1;36m║\n"
	@printf "  ║\033[0m  make lab01        Beginner  (DVWA+Splunk)   \033[1;36m║\n"
	@printf "  ║\033[0m  make lab02        Intermediate (JWT+SSRF)   \033[1;36m║\n"
	@printf "  ║\033[0m  make lab03        Advanced  (PWN+AI)        \033[1;36m║\n"
	@printf "  ║\033[0m  make lab04        Expert    (K8s+Falco)     \033[1;36m║\n"
	@printf "  ║\033[0m  make all          Labs 1-3 automático       \033[1;36m║\n"
	@printf "  ║\033[0m  make status       Estado de contenedores    \033[1;36m║\n"
	@printf "  ║\033[0m  make stop         Detener todos             \033[1;36m║\n"
	@printf "  ║\033[0m  make clean        Limpiar volúmenes         \033[1;36m║\n"
	@printf "  ╚══════════════════════════════════════════════╝\033[0m\n\n"

check-deps:
	@bash common/scripts/check-deps.sh

lab01: check-deps
	@echo "🚀  Lab 01 — Beginner..."
	@cd lab01 && docker compose --env-file .env up -d --build
	@echo "✅  DVWA → http://localhost:8080 | Splunk → http://localhost:8000 | API → http://localhost:5000"

lab02: check-deps
	@echo "🚀  Lab 02 — Intermediate..."
	@cd lab02 && docker compose --env-file .env up -d --build
	@echo "✅  API → https://localhost:9443 | Forensics → http://localhost:9090 | Volatility → http://localhost:8888"

lab03: check-deps
	@echo "🚀  Lab 03 — Advanced..."
	@cd lab03 && docker compose --env-file .env up -d --build
	@echo "✅  PWN-x64 → nc localhost 4444 | AI → http://localhost:8181 | Kibana → http://localhost:5601"

lab04: check-deps
	@bash lab04/setup-k8s.sh

all: check-deps
	@$(MAKE) lab01
	@$(MAKE) lab02
	@$(MAKE) lab03
	@echo "⚠️   Lab04 requiere Kind+Terraform. Ejecuta: make lab04"

status:
	@docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker no responde"

stop:
	@for lab in lab01 lab02 lab03; do \
	  if [ -f $$lab/docker-compose.yml ]; then \
	    cd $$lab && docker compose down 2>/dev/null || true && cd ..; \
	  fi; \
	done
	@kind delete cluster --name lab-expert 2>/dev/null || true
	@echo "✅  Todos los labs detenidos"

clean: stop
	@docker system prune -f --volumes 2>/dev/null || true
	@echo "✅  Limpieza completa"
