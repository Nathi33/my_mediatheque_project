from django import forms


class Creationmembre(forms.Form):
    name = forms.CharField(
        required=True,
        label="Nom",
        error_messages={
            'required': "Le champ 'Nom' est obligatoire"
        }
    )
    first_name = forms.CharField(
        required=True,
        label="Prénom",
        error_messages={
            'required': "Le champ 'Prénom' est obligatoire"
        }
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide"
        }
    )
    phone = forms.CharField(
        required=True,
        label="Téléphone",
        error_messages={
            'required': "Le champ 'Téléphone' est obligatoire"
        }
    )



class Updatemembre(forms.Form):
    name = forms.CharField(
        required=False,
        label="Nom",
        error_messages={
            'required': "Le champ 'Nom' est obligatoire"
        }
    )
    first_name = forms.CharField(
        required=False,
        label="Prénom",
        error_messages={
            'required': "Le champ 'Prénom' est obligatoire"
        }
    )
    email = forms.EmailField(
        required=False,
        label="Email",
        error_messages={
            'invalid': "Veuillez entrer une adresse email valide"
        }
    )
    phone = forms.CharField(
        required=False,
        label="Téléphone",
        error_messages={
            'required': "Le champ 'Téléphone' est obligatoire"
        }
    )