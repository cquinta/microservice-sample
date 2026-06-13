while true; do curl -X 'POST' 'http://localhost:8000/allops' \
                    -H 'accept: application/json' \
                    -H 'Content-Type: application/json' \
                    -d "{\"a\": $((RANDOM % 101)), \"b\": $((RANDOM % 101))}"; \
                     sleep 1; \
            done