from django import forms
from team.models import PlayerHistory, Matches


class PlayerHistoryForm(forms.ModelForm):
    class Meta:
        model = PlayerHistory
        fields = '__all__'


class MatchForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = '__all__'

# class PointsTableForm(forms.ModelForm):
#     class Meta:
#         model = PointsTable
#         fields = '__all__'
