

# def increment_app_id():
#     last_app = Appointment.objects.all().order_by('id').last()
#     if not last_app:
#         return 'DMAPP0000001'
#     app_id = last_app.appointment_id
#     app_int = int(app_id.split('DMAPP')[-1])
#     width = 7
#     new_app_int = app_int + 1
#     formatted = (width - len(str(new_app_int))) * "0" + str(new_app_int)
#     new_app_no = 'DMAPP' + str(formatted)
#     return new_app_no  


# def increment_capp_id():
#     last_app = CorporateAppointment.objects.all().order_by('id').last()
#     if not last_app:
#         return 'DMCAP0000001'
#     app_id = last_app.appointment_id
#     app_int = int(app_id.split('DMCAP')[-1])
#     width = 7
#     new_app_int = app_int + 1
#     formatted = (width - len(str(new_app_int))) * "0" + str(new_app_int)
#     new_app_no = 'DMCAP' + str(formatted)
#     return new_app_no  

# def increment_app_no():
#     last_app = Appointment.objects.all().order_by('appointment_no').last()
#     if not last_app:
#         return 'DMAPN0000001'
#     app_id = last_app.appointment_no
#     app_int = int(app_id.split('DMAPN')[-1])
#     width = 7
#     new_app_int = app_int + 1
#     formatted = (width - len(str(new_app_int))) * "0" + str(new_app_int)
#     new_app_no = 'DMAPN' + str(formatted)
#     return new_app_no

# def increment_capp_no():
#     last_app = CorporateAppointment.objects.all().order_by('appointment_no').last()
#     if not last_app:
#         return 'DMCPN0000001'
#     app_id = last_app.appointment_no
#     app_int = int(app_id.split('DMCPN')[-1])
#     width = 7
#     new_app_int = app_int + 1
#     formatted = (width - len(str(new_app_int))) * "0" + str(new_app_int)
#     new_app_no = 'DMCPN' + str(formatted)
#     return new_app_no


# def increment_invoice_number():
#     last_invoice = ICInvoice.objects.all().order_by('id').last()
#     if not last_invoice:
#         return 'DMINV0000001'
#     invoice_no = last_invoice.invoice_number
#     invoice_int = int(invoice_no.split('DMINV')[-1])
#     width = 7
#     new_invoice_int = invoice_int + 1
#     formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
#     new_invoice_no = 'DMINV' + str(formatted)
#     return new_invoice_no  

# def increment_cinvoice_number():
#     last_invoice = CCInvoice.objects.all().order_by('id').last()
#     if not last_invoice:
#         return 'DMCNV0000001'
#     invoice_no = last_invoice.invoice_number
#     invoice_int = int(invoice_no.split('DMCNV')[-1])
#     width = 7
#     new_invoice_int = invoice_int + 1
#     formatted = (width - len(str(new_invoice_int))) * "0" + str(new_invoice_int)
#     new_invoice_no = 'DMCNV' + str(formatted)
#     return new_invoice_no  

# def increment_ico_id():
#     last_ico = ICOrders.objects.all().order_by('id').last()
#     if not last_ico:
#         return 'DMICO0000001'
#     ico_id = last_ico.order_number
#     ico_int = int(ico_id.split('DMICO')[-1])
#     width = 7
#     new_ico_int = ico_int + 1
#     formatted = (width - len(str(new_ico_int))) * "0" + str(new_ico_int)
#     new_ico_no = 'DMICO' + str(formatted)
#     return new_ico_no  
