from booking.booking import Booking
try:
    with Booking() as bot:
        bot.land_first_page()
        bot.exit_signup()
        bot.change_currency(currency='USD')
        bot.select_place_to_go(place_to_go='Delhi')
        bot.select_date(check_in_date='2024-07-02', check_out_date='2024-07-04')
        bot.select_adults(10)
        bot.click_search()
        # bot.refresh() # a workaround to let our bot to grab the data properly 
        bot.apply_filtration()
        bot.report_results()
except Exception as e:
    if 'in PATH' in str(e):
        print(
            'You are trying to run the bot from command line \n'
            'Please add to PATH your Selenium Drivers \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:path-to-your-folder \n \n'
            'Linux: \n'
            '    PATH=$PATH:/path/toyour/folder/ \n'
        )
    else:
        raise
# inst = Booking()
# inst.land_first_page()