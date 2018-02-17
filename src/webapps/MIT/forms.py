from django import forms

from MIT.models import *
import datetime

class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['creator','counter']

    def clean(self):
        # Confirms that the username is not already present in the
        # User model database.
        cleaned_data = super(CreateGameForm, self).clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time > end_time:
        	raise forms.ValidationError("The start time should not be after end time.")
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        print name
        if Game.objects.filter(name__exact=name):
        	raise forms.ValidationError("Game name is already taken.")
        return name

    def clean_starting_balance(self):
        starting_balance = self.cleaned_data.get('starting_balance')
        if starting_balance <= 0.0:
        	raise forms.ValidationError("The starting balance should large than 0")
        return starting_balance

    def clean_interest_rate(self):
        interest_rate = self.cleaned_data.get('interest_rate')

        if interest_rate <= 0:
        	raise forms.ValidationError("The interest rate should large than 0")
        return interest_rate


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ['creator','game', 'transaction_time']

    def clean_transaction_type(self):
        transaction_type = self.cleaned_data.get('transaction_type')

        if transaction_type != "BUY" and transaction_type != "SELL" and transaction_type != "SHORT" and \
        transaction_type != "COVER"  and transaction_type != "BUY LIMIT" and transaction_type != "BUY STOP" and \
        transaction_type != "SELL LIMIT" and transaction_type != "SELL STOP" and transaction_type != "SHORT LIMIT" and \
        transaction_type != "SHORT STOP"  and transaction_type != "COVER STOP"  and transaction_type != "COVER LIMIT":
            raise forms.ValidationError("Please use valid transaction type")

        return transaction_type

    def clean_shares(self):
        shares = self.cleaned_data.get('shares')
        if shares <= 0.0:
        	raise forms.ValidationError("The transaction amount should large than 0")
        return shares

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email', 'password')
        widgets = {
            'username':forms.TextInput(attrs={'placeholder' : 'Username'}),
            'email':forms.TextInput(attrs={'placeholder' : 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder' : 'Password'}),
            }
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={'placeholder' : 'Confirm password'}),label='Confirm password')


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")
        return email

    def save(self):
        new_user = User.objects.create_user(username = self.cleaned_data['username'], \
                                            password = self.cleaned_data['password'], \
                                            email = self.cleaned_data['email'])
        new_user.is_active = False
        new_user.save()
        return new_user
