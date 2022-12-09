if [ ! -d "dist" ]; then
    npm run build
fi

npm run preview