module.exports = {
  apps: [
    {
      name: "food",
      script: "python3",
      args: "manage.py runserver 0.0.0.0:8000",
      cwd: "/home/ubuntu/dir/food",
      interpreter: "none",
      autorestart: true,
      watch: false,
      env: {
        DJANGO_SETTINGS_MODULE: "restaurants.settings",
      },
    },
  ],
};