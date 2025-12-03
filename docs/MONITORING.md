# NFL SIM Monitoring Setup

Complete monitoring solution for the NFL SIM application using Prometheus, Grafana, and associated exporters.

## Architecture

```text
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Grafana   │────>│  Prometheus  │<────│   Backend   │
│ (Dashboard) │     │  (Metrics)   │     │     API     │
└─────────────┘     └──────────────┘     └─────────────┘
                           ↑
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────────┐      ┌──────────────┐   ┌─────────────┐
   │  Node  │      │  PostgreSQL  │   │  cAdvisor   │
   │Exporter│      │   Exporter   │   │ (Container) │
   └────────┘      └──────────────┘   └─────────────┘
```

## Quick Start

### 1. Start Monitoring Stack

```bash
# Start all monitoring services
docker-compose -f docker-compose.monitoring.yml up -d

# Check service status
docker-compose -f docker-compose.monitoring.yml ps
```

### 2. Access Dashboards

- **Grafana**: <http://localhost:3001>

  - Username: `admin`
  - Password: `admin` (change on first login)

- **Prometheus**: <http://localhost:9090>

- **AlertManager**: <http://localhost:9093>

- **Node Exporter Metrics**: <http://localhost:9100/metrics>

- **cAdvisor**: <http://localhost:8080>

### 3. Import Dashboard

The NFL SIM dashboard is automatically provisioned at startup. Access it via:

1. Open Grafana (<http://localhost:3001>)
2. Navigate to **Dashboards** → **Browse**
3. Select **"NFL SIM - Application Overview"**

## Components

### Prometheus

#### Metrics Collection Engine

- Scrapes metrics from backend API, database, and system
- Stores time-series data
- Evaluates alerting rules
- Retention: 30 days (configurable)

**Configuration**: `monitoring/prometheus.yml`

### Grafana

#### Visualization and Dashboarding

- Pre-built dashboard for NFL SIM metrics
- Real-time monitoring
- Alert visualization
- Customizable panels

**Configuration**: `monitoring/grafana-dashboard.json`

### AlertManager

#### Alert Routing and Notification

- Routes alerts to appropriate teams
- Groups and deduplicates alerts
- Supports email, Slack, PagerDuty
- Inhibition rules to reduce noise

**Configuration**: `monitoring/alertmanager.yml`

### Node Exporter

#### System Metrics

Collects:

- CPU usage
- Memory usage
- Disk I/O
- Network statistics
- Filesystem metrics

### PostgreSQL Exporter

#### Database Metrics

Collects:

- Active connections
- Query performance
- Table sizes
- Index usage
- Lock statistics
- Replication lag

### cAdvisor

#### Container Metrics

Collects:

- Container CPU
- Container memory
- Network usage
- Filesystem usage

## Key Metrics

### API Performance

| Metric                               | Description         | Alert Threshold |
| ------------------------------------ | ------------------- | --------------- |
| `http_requests_total`                | Total HTTP requests | -               |
| `http_request_duration_seconds`      | Request latency     | p95 > 1s        |
| `http_requests_total{status=~"5.."}` | Server errors       | Rate > 5%       |

### Database Health

| Metric                              | Description        | Alert Threshold |
| ----------------------------------- | ------------------ | --------------- |
| `pg_stat_database_numbackends`      | Active connections | > 80% of max    |
| `pg_stat_statements_mean_exec_time` | Avg query time     | > 1000ms        |
| `pg_database_size_bytes`            | Database size      | -               |

### System Resources

| Metric                           | Description      | Alert Threshold |
| -------------------------------- | ---------------- | --------------- |
| `node_cpu_seconds_total`         | CPU usage        | > 80%           |
| `node_memory_MemAvailable_bytes` | Available memory | < 15%           |
| `node_filesystem_avail_bytes`    | Disk space       | < 15%           |

### Simulation Engine

| Metric                        | Description          | Alert Threshold |
| ----------------------------- | -------------------- | --------------- |
| `simulation_duration_seconds` | Game simulation time | p95 > 60s       |
| `simulation_total`            | Total simulations    | -               |
| `simulation_failures_total`   | Failed simulations   | Rate > 1%       |

## Alerts

### Critical Alerts

Immediate notification to on-call team:

- **HighErrorRate**: API error rate > 5%
- **DatabaseConnectionPoolExhausted**: > 80% connections used
- **HighSimulationFailureRate**: Simulation failure rate > 1%

### Warning Alerts

Team notification:

- **SlowResponseTime**: p95 latency > 1s
- **SlowQueries**: Average query time > 1000ms
- **HighCPUUsage**: CPU > 80% for 10 minutes
- **HighMemoryUsage**: Memory > 85%

### Configuration

Edit alert rules in `monitoring/alert_rules.yml`

## Customization

### Add Custom Metrics

In your FastAPI backend:

```python
from prometheus_client import Counter, Histogram

# Define custom metrics
simulation_counter = Counter(
    'simulation_total',
    'Total number of simulations run',
    ['team_home', 'team_away']
)

simulation_duration = Histogram(
    'simulation_duration_seconds',
    'Time spent simulating a game',
    buckets=[1, 5, 10, 30, 60, 120]
)

# Use in code
@router.post("/simulate-game")
def simulate_game(home_team: int, away_team: int):
    with simulation_duration.time():
        result = run_simulation(home_team, away_team)

    simulation_counter.labels(
        team_home=home_team,
        team_away=away_team
    ).inc()

    return result
```

### Create Custom Dashboard

1. Open Grafana → Create → Dashboard
2. Add Panel
3. Select data source: Prometheus
4. Enter PromQL query
5. Customize visualization
6. Save dashboard

Example PromQL queries:

```promql
# Request rate by endpoint
rate(http_requests_total[5m])

# Response time percentiles
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate percentage
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100
```

## Notification Setup

### Email Notifications

Edit `monitoring/alertmanager.yml`:

```yaml
global:
  smtp_smarthost: "smtp.gmail.com:587"
  smtp_from: "your-email@gmail.com"
  smtp_auth_username: "your-email@gmail.com"
  smtp_auth_password: "your-app-password"
```

### Slack Notifications

1. Create a Slack webhook: <https://api.slack.com/messaging/webhooks>
2. Edit `monitoring/alertmanager.yml`:

```yaml
slack_configs:
  - api_url: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    channel: "#nfl-sim-alerts"
```

### PagerDuty Integration

1. Get PagerDuty integration key
2. Edit `monitoring/alertmanager.yml`:

```yaml
pagerduty_configs:
  - service_key: "your-pagerduty-service-key"
```

## Troubleshooting

### Metrics Not Appearing

1. **Check backend is exposing metrics**:

   ```bash
   curl http://localhost:8000/metrics
   ```

2. **Verify Prometheus is scraping**:

   - Open <http://localhost:9090/targets>
   - Check if backend target is UP

3. **Check Prometheus logs**:

   ```bash
   docker logs nfl-sim-prometheus
   ```

### Database Metrics Missing

1. **Verify PostgreSQL exporter connection**:

   ```bash
   docker logs nfl-sim-postgres-exporter
   ```

2. **Check DATA_SOURCE_NAME** in `docker-compose.monitoring.yml`

### Grafana Dashboard Not Loading

1. **Check Grafana logs**:

   ```bash
   docker logs nfl-sim-grafana
   ```

2. **Verify dashboard file** in `monitoring/grafana-dashboard.json`

3. **Manually import dashboard**:
   - Grafana → Dashboards → Import
   - Upload `grafana-dashboard.json`

## Maintenance

### Backup Grafana Dashboards

```bash
# Export dashboard
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://localhost:3001/api/dashboards/uid/DASHBOARD_UID \
  > dashboard_backup.json
```

### Clear Old Metrics

Prometheus automatically manages retention (default: 30 days).

To adjust:

```yaml
# In docker-compose.monitoring.yml
command:
  - "--storage.tsdb.retention.time=90d" # 90 days
```

### Update Alert Rules

1. Edit `monitoring/alert_rules.yml`
2. Reload Prometheus:

   ```bash
   docker-compose -f docker-compose.monitoring.yml restart prometheus
   ```

## Production Considerations

1. **Change default passwords** (Grafana admin password)
2. **Enable HTTPS** for Grafana
3. **Set up persistent volumes** for metrics data
4. **Configure backup** for Grafana dashboards and Prometheus data
5. **Set resource limits** in docker-compose
6. **Enable authentication** for Prometheus/AlertManager
7. **Use secret management** for sensitive credentials

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
