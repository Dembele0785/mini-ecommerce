from app import create_app

print("--- Starting application ---")
app = create_app()
print("--- Application created ---")

if __name__ == '__main__':
    print("--- Running main block ---")
    app.run(debug=True)
else:
    print(f"--- Not in main block, __name__ is {__name__} ---")