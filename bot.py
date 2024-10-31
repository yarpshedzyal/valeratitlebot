import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from modules.title_scraper import scrape_title  # Import the scrape_title function
import time
import asyncio

# Function to read the token from config.txt
def read_token_from_file(filename):
    with open(filename, 'r') as file:
        return file.readline().strip()

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Please send me a CSV file containing links.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.document.get_file()
    await file.download_to_drive('links.csv')
    await update.message.reply_text("File received! Scraping titles...")

    # Read the CSV file with Pandas
    df = pd.read_csv('links.csv')

    # Check if the 'links' column exists
    if 'links' in df.columns:
        titles = []
        start_time = time.time()  # Start the timer
        for index, link in enumerate(df['links']):
            title = scrape_title(link)
            titles.append(title)
            time.sleep(3)
            # Pause every 20 links
            if (index + 1) % 20 == 0:
                await update.message.reply_text(f"Processed {index + 1} links. Taking a 30-second break...")
                await asyncio.sleep(30)  # Pause for 30 seconds

        # Create a new DataFrame for the results
        results_df = pd.DataFrame({'Link': df['links'], 'Title': titles})

        # Write the results to a new CSV file
        results_df.to_csv('titles.csv', index=False)

        # Send the results back to the user
        await update.message.reply_document(document=open('titles.csv', 'rb'))

        # Print the total time taken
        total_time = time.time() - start_time
        await update.message.reply_text(f"Processing complete! Total time taken: {total_time:.2f} seconds.")
    else:
        await update.message.reply_text("The CSV file must contain a column named 'links'.")


# Main function to run the bot
def main():
    # Read the bot token from config.txt
    token = read_token_from_file('config.txt')

    # Create the bot application with your token
    application = ApplicationBuilder().token(token).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.MimeType("text/csv"), handle_document))

    # Run the bot until you stop it manually
    application.run_polling()

# Run the main function only if this module is executed directly
if __name__ == "__main__":
    main()
