# GET DEMERIT POINTS APPLICATION ####
# take driving speed in either int or float number value
# and determine discretionary or mandatory penalty points
# with checkbox holiday period available.  

import os
from flask import Flask, render_template, request, flash

SUCCESS_MSG = 'success'
WARNING_MSG = 'warning'
KEY_SIZE = 24
HTML_TEMPLATE = 'flask_formats.html'

# Create Flask instance and set the session key
app = Flask(__name__)
app.secret_key = os.urandom(KEY_SIZE)

# handle any other url entered:
@app.errorhandler(404) 
def page_not_found(e): 
  return render_template('404_with_timer.html') 

def get_demerit_points(driving_speed, speed_limit, holiday_period=False):
    """
    Works out the demerit (penalty) points for a driving 
    speed in a particular speed limited zone.
    """
    speed_over = driving_speed - speed_limit
    penalty_points = 0
    mandatory_penalty = False
    if speed_over < 0:
        mandatory_penalty = False
        penalty_points = 0
    elif speed_over == 0:
        mandatory_penalty = False
        penalty_points = 0
    else:
        if holiday_period:
            if speed_over <= 4:
                mandatory_penalty = False
                penalty_points = 10
            elif speed_over <= 10:
                mandatory_penalty = True
                penalty_points = 10
            elif speed_over <= 20:
                mandatory_penalty = True
                penalty_points = 20
            elif speed_over <= 30:
                mandatory_penalty = True
                penalty_points = 30
            else:
                mandatory_penalty = True
                penalty_points = 50
        else:
            if speed_over <= 5:
                mandatory_penalty = False
                penalty_points = 10
            elif speed_over <= 10:
                mandatory_penalty = True
                penalty_points = 10
            elif speed_over <= 20:
                mandatory_penalty = True
                penalty_points = 20
            elif speed_over <= 30:
                mandatory_penalty = True
                penalty_points = 30
            else:
                mandatory_penalty = True
                penalty_points = 50
    answer = (mandatory_penalty, penalty_points)
    return answer

@app.route('/', methods = ['POST', 'GET'])
def home():
    """ Home page handler """

    print(f'DEBUG. Function received http method type: {request.method}')
    
    if request.method == 'POST':
        # Get the data that has been sent via http post
        driving = request.form.get('form_first_number')
        limit = request.form.get('form_second_number')
        is_holiday = request.form.get('form_tickbox1')
        print(f'{is_holiday=}')
              
        if driving != '' and limit != '':
            # Data has been submitted
            if driving.replace('.','').isdigit() and limit.isdigit():
                # Numerical fields are digits now need check to see if 
                # we should convert 'driving' to a float or an int 
                if '.' not in driving:
                    driving = int(driving)
                else:
                    driving = float(driving)
                limit = int(limit)
                # Compare the values received and return the results to the browser
                result = get_demerit_points(driving, limit, is_holiday)
                if driving > limit:
                    if result[0] == True:  
                        msg = f'The mandatory penalty for driving at {driving}km/h in a {limit}km/h zone is {result[1]} points.'
                    else:
                        msg = f'The discretional penalty for driving at {driving}km/h in a {limit}km/h zone is {result[1]} points.'
                else:
                    msg = f'{driving}km/h in a {limit}km/h zone is not speeding.'
                flash(msg, SUCCESS_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit points calculator', form_first_number=driving, form_second_number=limit, form_tickbox1=is_holiday)
            else:
                # Not digits
                flash(f'Numbers only please.', WARNING_MSG)
        # if driving speed or speed limit is not received:
        elif driving != '':
            flash('Please enter a speed limit', WARNING_MSG)
        elif limit != '':
            flash('Please enter a driving speed', WARNING_MSG)

        else:
            # Not all the data was received
            flash('Please enter a driving speed and speed limit.', WARNING_MSG)

    return render_template(HTML_TEMPLATE, title='Demerit points calculator')

if __name__ == '__main__':
    app.run()
