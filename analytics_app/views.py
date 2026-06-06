from django.shortcuts import render

def analytics(request):
    context = {
        'vendors': 10,
        'purchase_orders': 15,
        'invoices': 20,
    }

    return render(
        request,
        'analytics/dashboard_charts.html',
        context
    )