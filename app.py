import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Dash app
app = dash.Dash(__name__, assets_folder='assets')

# Define some common styles
tab_style = {
    'backgroundColor': '#f9f9f9',
    'padding': '6px',
    'fontWeight': 'bold',
    'color': '#333',
}

tab_selected_style = {
    'backgroundColor': '#d9edf7',
    'borderTop': '1px solid #007bff',
    'padding': '6px',
}

info_quiz_style = {
    'border': '1px solid #dfe3e6',
    'padding': '15px',
    'borderRadius': '5px',
    'backgroundColor': '#f4f4f4',
    'margin': '10px',
    'color': '#333',
    'fontSize': '16px',
}

question_style = {
    'margin': '10px 0',
}

home_title_style = {
    'textAlign': 'center',
    'color': 'white',
    'fontSize': '36px', 
    'fontWeight': 'bold',  
    'margin': '20px 0',  
    'textShadow': '2px 2px 4px #000000'
}

login_controls_style = {
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center',
    'height': '100vh'
}

login_message_style = {
    'textAlign': 'center',
    'marginBottom': '10px',
    'fontStyle': 'italic',
    'fontWeight': 'bold'
}

login_page_style = {
    'display': 'flex',
    'flexDirection': 'column',
    'justifyContent': 'center',
    'alignItems': 'center',
    'height': '100vh',
    'backgroundImage': 'url(/assets/pexels-pixabay-257937.jpg)',
    'backgroundSize': 'cover',
    'backgroundPosition': 'center',
    'backgroundRepeat': 'no-repeat'
}

# Correct answers for the quiz
correct_answers = {
    'quiz-question-1': 'Q1B',
    'quiz-question-2': 'Q2C',
    'quiz-question-3': 'Q3A',
    'quiz-question-4': 'Q4C',
    'quiz-question-5': 'Q5C',
    'quiz-question-6': 'Q6A',
    'quiz-question-7': 'Q7C',
    'quiz-question-8': 'Q8C',
    'quiz-question-9': 'Q9B',
    'quiz-question-10':'Q10C',
}

USER_DB_FILE = 'user_db.json'

def load_user_db():
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, 'r') as file:
        return json.load(file)

def save_user_db(user_db):
    with open(USER_DB_FILE, 'w') as file:
        json.dump(user_db, file)

# Define the app layout
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Home', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Information', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Quiz', value='tab-5', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs-content-example'),
    html.Div(id='login-controls', style=login_page_style, children=[
        html.Div("Please create an account or proceed as guest.", style=login_message_style),
        dcc.Input(id='username', type='text', placeholder='Username', style={'margin': '10px'}),
        dcc.Input(id='password', type='password', placeholder='Password', style={'margin': '10px'}),
        html.Button('Login', id='login-button', n_clicks=0, style={'margin': '10px'}),
        html.Button('Create Account', id='create-account-button', n_clicks=0, style={'margin': '10px'}),
        html.Button('Continue as Guest', id='guest-button', n_clicks=0, style={'margin': '10px'}),
        html.Div(id='login-output')
    ]),
    html.Div(id='quiz-container')
])


# Callback to display the quiz when the "Start Quiz" button is clicked
@app.callback(
    [Output('quiz-container', 'style'),
     Output('quiz-container', 'children')],
    [Input('start-quiz-button', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_quiz_visibility_and_content(n_clicks):
    if n_clicks > 0:
        # Return the style to show the quiz and the quiz content
        return {'display': 'block'}, get_quiz_content()
    # Return the style to hide the quiz and no content
    return {'display': 'none'}, None

def get_quiz_content():
    # Construct the quiz content layout
    return html.Div([
        html.Div([
            html.Label('What is Phishing?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-1',
                options=[
                    {'label': 'A scam where attackers hack your phone', 'value': 'Q1A'},
                    {'label': 'A scam where attackers send fraudulent messages', 'value': 'Q1B'},
                    {'label': 'A scam technique that involves physical media', 'value': 'Q1C'},
                ],
                value='Q1A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What should you do if you receive an unexpected email attachment?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-2',
                options=[
                    {'label': 'Open it immediately to see what it is', 'value': 'Q2A'},
                    {'label': 'Delete the email without opening the attachment', 'value': 'Q2B'},
                    {'label': 'Verify the sender’s identity before opening', 'value': 'Q2C'},
                ],
                value='Q2A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Ransomware?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-3',
                options=[
                    {'label': 'A scam where attackers demand payment in exchange for not releasing sensitive information', 'value': 'Q3A'},
                    {'label': 'A scam where attackers pretend to be a romantic interest to obtain money or personal information', 'value': 'Q3B'},
                    {'label': 'A scam where attackers use fake job offers to trick individuals into providing personal information', 'value': 'Q3C'},
                ],
                value='Q3A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Vishing?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-4',
                options=[
                    {'label': 'A scam where attackers use fake websites to steal personal information', 'value': 'Q4A'},
                    {'label': ' A scam where attackers send malicious software via email attachments', 'value': 'Q4B'},
                    {'label': 'A scam where attackers impersonate legitimate organizations via phone calls to obtain sensitive information', 'value': 'Q4C'},
                ],
                value='Q4A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Identity Theft?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-5',
                options=[
                    {'label': 'A scam where attackers send fake lottery winnings notifications to steal money', 'value': 'Q5A'},
                    {'label': 'A scam where attackers hijack your social media accounts to spread false information', 'value': 'Q5B'},
                    {'label': 'A scam where attackers steal personal information to impersonate someone else for financial gain', 'value': 'Q5C'},
                ],
                value='Q5A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Social Engineering?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-6',
                options=[
                    {'label': 'A scam where attackers trick individuals into revealing sensitive information through psychological manipulation', 'value': 'Q6A'},
                    {'label': 'A scam where attackers use software vulnerabilities to gain unauthorized access to computer systems', 'value': 'Q6B'},
                    {'label': 'A scam where attackers pretend to be a legitimate organization to obtain login credentials', 'value': 'Q6C'},
                ],
                value='Q6A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What strategies should you be aware of to avoid falling victim to a Smishing attempt?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-7',
                options=[
                    {'label': 'Visit the links in the text to check the senders identity', 'value': 'Q7A'},
                    {'label': 'Respond to the message  and send a message back to the sender.', 'value': 'Q7B'},
                    {'label': 'Verify the senders identity through official contact methods, not through numbers or links provided in the text.', 'value': 'Q7C'},
                ],
                value='Q7A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Pharming?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-8',
                options=[
                    {'label': 'A scam where attackers send fraudulent text messages to steal personal information', 'value': 'Q8A'},
                    {'label': 'A scam where attackers create fake social media profiles to manipulate individuals emotionally', 'value': 'Q8B'},
                    {'label': 'A scam where attackers manipulate DNS servers to redirect users to fake websites without their knowledge', 'value': 'Q8C'},
                ],
                value='Q8A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Smishing?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-9',
                options=[
                    {'label': 'A scam where attackers use fake job offers to steal money or personal information', 'value': 'Q9A'},
                    {'label': 'A scam where attackers send fraudulent messages via SMS (text) to trick individuals into providing personal information', 'value': 'Q9B'},
                    {'label': 'A scam where attackers create fake websites to trick users into revealing sensitive information', 'value': 'Q9C'},
                ],
                value='Q9A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Div([
            html.Label('What is Malware?', style=question_style),
            dcc.RadioItems(
                id='quiz-question-10',
                options=[
                    {'label': 'A scam where attackers manipulate search engine results to promote fake products or services', 'value': 'Q10A'},
                    {'label': 'A scam where attackers use fake job offers to steal money or personal information', 'value': 'Q10B'},
                    {'label': 'Software designed to infiltrate or damage a computer system without the owners consent', 'value': 'Q10C'},
                ],
                value='Q10A',
                labelStyle={'display': 'block'}
            ),
        ], style=info_quiz_style),
        html.Button('Submit', id='submit-val', n_clicks=0, style={'backgroundColor': '#007bff', 'color': 'white'}),
        html.Div(id='quiz-result', style={'marginTop': '20px'})
    ])

# Callback to handle quiz submission and scoring
@app.callback(
    Output('quiz-result', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('quiz-question-1', 'value'),
     State('quiz-question-2', 'value'),
     State('quiz-question-3', 'value'),
     State('quiz-question-4', 'value'),
     State('quiz-question-5', 'value'),
     State('quiz-question-6', 'value'),
     State('quiz-question-7', 'value'),
     State('quiz-question-8', 'value'),
     State('quiz-question-9', 'value'),
     State('quiz-question-10', 'value')],
    prevent_initial_call=True
)
def update_result(n_clicks, *args):
    if n_clicks == 0:
        raise PreventUpdate
    # args will contain all the answer values as a tuple
    score = sum(args[i] == correct_answers[f'quiz-question-{i+1}'] for i in range(10))
    return f'Your score is {score} out of 10.'

@app.callback(
    [Output('tabs-content-example', 'children'),
     Output('tabs-example', 'value'),
     Output('login-controls', 'style'),
     Output('login-output', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('create-account-button', 'n_clicks'),
     Input('guest-button', 'n_clicks'),
     Input('tabs-example', 'value')],  # Adding this to trigger on tab change as well
    [State('username', 'value'),
     State('password', 'value')],
    prevent_initial_call=True
)
def handle_combined_actions(login_n_clicks, create_n_clicks, guest_n_clicks, tab_value, username, password):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    login_controls_style = {'display': 'none'}  # Assume user interaction hides the controls
    message = ""
    active_tab = tab_value

    if triggered_id == 'login-button' and login_n_clicks:
        user_db = load_user_db()
        user = user_db.get(username)
        if user and check_password_hash(user['password'], password):
            message = 'Logged in successfully!'
            active_tab = 'tab-1'
        else:
            message = 'Incorrect username or password.'
            login_controls_style = {'display': 'block'}  # Show again if login failed

    elif triggered_id == 'create-account-button' and create_n_clicks:
        user_db = load_user_db()
        if username and password:
            if username in user_db:
                message = 'Username already exists.'
                login_controls_style = {'display': 'block'}  # Show again if username exists
            else:
                user_db[username] = {'password': generate_password_hash(password)}
                save_user_db(user_db)
                message = 'Account created successfully!'
                active_tab = 'tab-1'
        else:
            message = 'Please enter a username and password.'
            login_controls_style = {'display': 'block'}  # Show again if fields are empty

    elif triggered_id == 'guest-button' and guest_n_clicks:
        message = 'Continuing as guest. Your progress will not be saved.'
        active_tab = 'tab-1'

    return render_content(active_tab), active_tab, login_controls_style, message

def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H1('Internet Safety and Scam Awareness for Vulnerable Users', style=home_title_style),
            html.Div([
                html.P("The purpose of this project is to develop an interactive website that educates "
                       "vulnerable users about Internet Safety and common scams, including phishing, "
                       "smishing, vishing, and ransomware. The project aims to create a platform that "
                       "tests users' knowledge via a quiz and provides detailed information on "
                       "various common scam methods. The primary goal is to enhance users' "
                       "awareness and knowledge of internet safety, making them less susceptible to "
                       "online threats.",
                       style={'color': 'white', 'fontSize': 18})
            ], style={
                'position': 'absolute',
                'top': '50%',
                'left': '50%',
                'transform': 'translate(-50%, -50%)',
                'color': 'white',
                'textAlign': 'center',
                'width': '50%'
            }),
        ], style={
            'backgroundImage': 'url(/assets/Internet_Safety.jpg)',
            'backgroundSize': 'cover',
            'height': '100vh',
            'position': 'relative',
            'textColor': 'white'
        })
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Information on Common Scams and Techniques and Strategies to avoid becoming a victim'),
            html.Div([
                html.H4('Phishing'),
                html.P("Phishing is a form of cyber attack where attackers impersonate legitimate entities, such as banks, email providers, or government agencies, to deceive individuals into providing sensitive information such as usernames, passwords, credit card details, or other personal information. This is typically done through fraudulent emails, messages, or websites that appear to be from trusted sources. Phishing attacks often employ social engineering tactics to manipulate recipients into taking action, such as clicking on malicious links or downloading malicious attachments, thereby compromising their personal information or computer systems. The goal of phishing attacks is usually financial gain or unauthorized access to sensitive data but there are some strategies to avoid this scam."),
                html.P("1. Skepticism Towards Unsolicited Messages: Treat unexpected communications asking for personal information or urgent action with suspicion."),
            html.P("2. Sender Verification: Inspect the sender's email or contact details for any discrepancies or misspellings compared to legitimate contacts."),
            html.P("3. Spotting Message Red Flags: Look out for poor spelling, generic greetings, and pressure to act quickly, which are common in phishing attempts."),
            html.P("4. Avoiding Suspicious Links and Attachments: Don’t click on links or download files from messages that seem untrustworthy."),
            html.P("5. Independent Verification: If a message appears to be from a known company, verify its authenticity through official channels rather than replying directly."),
            html.P("6. Utilizing Two-Factor Authentication: Activate two-factor authentication for an added security layer on your accounts, reducing the risk even if your password is compromised."),
            html.P("7. Staying Informed: Keep up with the latest phishing methods to recognize potential scams more easily."),
                html.H4('Smishing'),
                html.P("Smishing is a type of phishing attack conducted via SMS (text message) or other messaging platforms. Attackers send fraudulent messages to trick individuals into revealing sensitive information or downloading malicious software onto their devices. Strategies to avoid Smishing include: "),
                html.P("1.Question Unexpected Texts: Be cautious with text messages from unknown numbers or unexpected messages asking for personal information or action."),
                html.P("2.Verify Senders Identity: If a text claims to be from a reputable source, verify through official contact methods, not through numbers or links provided in the suspicious text."),
                html.P("3.Strategies to avoid Phising also applicable."),
                html.H4('Vishing'),
                html.P("Vishing, or voice phishing, is a scam where attackers use phone calls or voice messages to impersonate legitimate organizations or authorities, aiming to deceive individuals into revealing sensitive information, such as passwords or financial details."),
                html.Img(src='/assets/istockphoto-1162424348-612x612.jpg', 
                         style={
                'height': 'auto',  # Keep the aspect ratio
                'width': '33.33%',    # Set width as a third of the parent div
            }),
            html.Img(src='/assets/istockphoto-1264113455-612x612.jpg',  
            style={
                'height': 'auto',  # Keep aspect ratio
                'width': '33.33%',  # Set each image to a third
            }
        ),
        html.Img(src='/assets/istockphoto-1463637004-612x612.jpg',  
            style={
                'height': 'auto',  # Keep aspect ratio
                'width': '33.33%',  # Set each image to a third
            }
        ),
        html.P("1. Be Wary of Unknown Callers: Treat unsolicited calls with skepticism, especially those requesting personal or financial information."),
        html.P("2. Keep Personal Information Private:Never share personal, financial, or security information in response to unsolicited calls."),
        html.P("3. Recognize Pressure Tactics: Scammers often create a sense of urgency. Be cautious of any caller pressuring immediate action."),
        html.P("4. Use Caller ID and Blocking: Employ caller ID and call-blocking services to filter out potential scammers."),
                html.H4('Ransomware'),
                html.P("Ransomware is a type of malware that encrypts files or locks computer systems, demanding payment (a ransom) from the victim in exchange for restoring access. It effectively holds the victim's data or device hostage until the ransom is paid."),
                html.P("1. Keep Software Up to Date: Regularly update all software, including antivirus programs, to protect against known vulnerabilities that ransomware could exploit."),
                html.P("2. Back Up Important Data: Regularly back up important files to an external drive or cloud storage that is not always connected to your network."),
                html.P("3. Use Reputable Antivirus Software: Install and maintain reputable security software that includes ransomware detection and removal features."),
                html.H4('Social Engineering'),
                html.P("Social engineering is the manipulation of people into giving up confidential information or access to systems, typically for malicious purposes, by exploiting human psychology rather than technical hacking methods."),
                html.H4('Spoofing'),
                html.P("Spoofing involves falsifying data to appear as someone or something else. In the context of cybersecurity, it often refers to techniques where attackers manipulate information such as email addresses, caller IDs, or website URLs to deceive recipients into thinking they are interacting with a legitimate source."),
                html.H4('Pharming'),
                html.P("Pharming is a cyber attack where attackers redirect website traffic from legitimate websites to fraudulent ones without the users' knowledge. This is typically achieved by compromising DNS servers or injecting malicious code into routers or other network devices. The goal is to steal sensitive information, such as login credentials or financial data, from unsuspecting users."),
                html.H4('Malware'),
                html.P("Malware, or 'malicious software,' refers to a variety of harmful programs created to disrupt, damage, or gain unauthorized access to computer systems. It encompasses a range of threats including viruses, worms, trojan horses, ransomware, and spyware, each designed with specific methods and malicious intents."),
            ])
        ])
    elif tab == 'tab-5':
        return html.Div([
            html.Button('Start Quiz', id='start-quiz-button', n_clicks=0, style={'margin-top': '20px'}),
            html.Div(id='quiz-container'),
            html.Div(id='quiz-result', style={'marginTop': '20px'})
        ])
    return html.Div()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)





