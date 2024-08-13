module.exports = {
    apps: [
        {
            script: 'app.py',
            interpreter: 'python',
            cron_restart: '0 7 * * *', // configurado diariamente para iniciar todos os dias às 7h.
            name: 'script-maintenance-iot',
        }
    ]
}

// pm2 start ecosystem.config.ts