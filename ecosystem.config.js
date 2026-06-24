module.exports = {
  apps: [
    {
      name: "food",
      script: "gunicorn",
      args: "-c gunicorn.conf.py",
      cwd: "/home/ubuntu/dir/food",
      interpreter: "none",
      autorestart: true,
      watch: false,
    },
  ],
};