from django.forms import Form,fields,widgets


class GroupADD(Form):
    gname = fields.CharField(max_length=16,min_length=2,
                             error_messages={'required':'组用户名不能为空',
                                             'min_length':'用户名至少6个字符'},
        widget=widgets.TextInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))

class GUserADD(Form):
    uid = fields.CharField(error_messages={'required':'用户id不能为空',
                                             },
        widget=widgets.NumberInput(attrs={'class':'form-control','aria-describedby':'basic-addon1'}))