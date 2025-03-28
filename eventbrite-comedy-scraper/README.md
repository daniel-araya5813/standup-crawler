# Comedy Event Finder and Information Collector

This is a two-step tool that helps you find stand-up comedy events in Ontario, Canada, and collect detailed information about them.

## What This Tool Does

1. **First Step**: Searches Eventbrite to find comedy events and saves their website addresses
2. **Second Step**: Visits each event website and collects detailed information like venue, date, price, etc.

## How to Use This Tool

### Before You Start

1. Make sure you have Python installed on your computer
2. Install the necessary components:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API key (copy from `.env.example`)
4. Run the setup script to create all needed folders:
   ```
   python Create_Directories.py
   ```

### Finding Comedy Events (Step 1)

Simply run:
```
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py
```

This will:
- Search for comedy events on Eventbrite
- Save all the event website addresses to a file in `Collected_Data/Discovered_Event_Websites/`

You can adjust how many pages to search by adding:
```
python First_Step_Find_All_Events/Run_This_First_To_Find_Events.py --start 1 --end 5
```

### Collecting Event Details (Step 2)

After step 1 is complete, run:
```
python Second_Step_Get_Event_Details/Run_This_Second_To_Get_Event_Details.py
```

This will:
- Visit each event website found in step 1
- Collect detailed information about each event
- Save all the information to a file in `Collected_Data/Complete_Event_Descriptions/`

## What's In Each Folder

- **First_Step_Find_All_Events**: Contains all the files needed for finding event websites
- **Second_Step_Get_Event_Details**: Contains all the files needed for collecting event information
- **Shared_Tools_Both_Steps_Use**: Contains tools used by both steps
- **Collected_Data**: Where all the information is stored
  - **Discovered_Event_Websites**: List of event websites found
  - **Complete_Event_Descriptions**: Detailed information about each event
- **Logs**: Records of what happened when you ran the tool

## Adjusting Settings

If you want to change how the tool works:

- For finding events: Edit `First_Step_Find_All_Events/Web_Browser_Configuration.py`
- For collecting information: Edit `Second_Step_Get_Event_Details/Smart_Text_Analyzer_Configuration.py`
- For general settings: Edit `Main_Settings.py`

## Need Help?

If you run into any problems, check the log files in the `Logs` folder to see what went wrong.