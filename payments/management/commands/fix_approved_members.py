from django.core.management.base import BaseCommand
from payments.models import Payment
from applications.models import ApplicationStatus


class Command(BaseCommand):
    help = 'Fix users with confirmed payments but not marked as approved members'

    def handle(self, *args, **options):
        # Get all confirmed payments
        confirmed_payments = Payment.objects.filter(is_confirmed=True)
        
        fixed_count = 0
        for payment in confirmed_payments:
            user = payment.application.user
            
            # If payment is confirmed but user is not approved, fix it
            if not user.is_approved_member:
                user.is_approved_member = True
                user.save()
                
                # Also update application status if needed
                if payment.application.status != ApplicationStatus.PAYMENT_CONFIRMED:
                    payment.application.status = ApplicationStatus.PAYMENT_CONFIRMED
                    payment.application.save()
                
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Fixed user: {user.email} - {payment.application.full_name}')
                )
        
        if fixed_count == 0:
            self.stdout.write(self.style.SUCCESS('No users needed fixing. All confirmed payments have approved members.'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully fixed {fixed_count} user(s)')
            )






