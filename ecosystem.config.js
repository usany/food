module.exports = {
  apps: [
    {
      name: "food",
      script: "gunicorn",
      args: "-c /home/ubuntu/food/gunicorn.conf.py restaurants.wsgi:application",      
      cwd: "/home/ubuntu/food",
      interpreter: "none",
      autorestart: true,
      watch: false,
    },
  ],
};