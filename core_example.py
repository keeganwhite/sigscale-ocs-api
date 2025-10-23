"""
Core OCS API Example - Focused on Essential Operations

This example demonstrates the three core operations:
1. SIM Card Creation (Service/Subscriber signup)
2. Product Subscription (Data purchase)
3. Balance Top-Up (Adding credits)

Based on the official SigScale OCS REST API test suite.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main example function demonstrating core OCS operations."""
    
    # Import here to avoid module-level import issues
    try:
        from sigscale_ocs import (
            OCSClient, 
            BalanceManagement, 
            ProductCatalog, 
            ProductInventory, 
            ServiceInventory
        )
    except ImportError:
        print("Error: sigscale-ocs package not found. Please install it with:")
        print("pip install -e .")
        sys.exit(1)

    # Check if required environment variables are set
    required_vars = ['SIGSCALE_OCS_URL', 'SIGSCALE_OCS_USERNAME', 'SIGSCALE_OCS_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set up your .env file with the required credentials.")
        print("See .env.example for reference.")
        sys.exit(1)

    print("Sigscale OCS Core Operations Example")
    print("=" * 40)

    # Initialize the OCS client
    try:
        client = OCSClient()
        print("Successfully connected to OCS API")
    except Exception as e:
        print(f"❌ Failed to connect to OCS API: {e}")
        sys.exit(1)

    # Initialize API modules
    balance = BalanceManagement(client)
    catalog = ProductCatalog(client)
    inventory = ProductInventory(client)
    service_inventory = ServiceInventory(client)

    try:
        # Step 1: List available offerings
        print("\n1. Available Product Offerings")
        print("-" * 30)
        offerings = catalog.list_offerings()
        if offerings:
            print(f"Found {len(offerings)} available offerings:")
            for offering in offerings[:3]:  # Show first 3
                print(f"  - {offering.get('name', 'N/A')} (ID: {offering.get('id', 'N/A')})")
            offering_id = offerings[0].get('id')
        else:
            print("❌ No offerings found. Cannot proceed with product creation.")
            return

        # Step 2: Create a service/subscriber (SIM card signup)
        print("\n2. Creating Service/Subscriber (SIM Card Signup)")
        print("-" * 45)
        service_data = {
            "name": "Example SIM Card",
            "description": "SIM card for demonstration",
            "status": "active",
            "serviceCharacteristic": [
                {
                    "name": "IMSI",
                    "value": "123456789012345"
                },
                {
                    "name": "Phone Number",
                    "value": "+1234567890"
                }
            ]
        }
        
        service_result = service_inventory.create_service(service_data)
        service_id = service_result.get('id')
        print(f"Created service/subscriber: {service_id}")

        # Step 3: Create a product subscription (data purchase)
        print("\n3. Creating Product Subscription (Data Purchase)")
        print("-" * 45)
        product_data = {
            "name": "Example Data Plan",
            "description": "Data subscription for demonstration",
            "productOffering": {"id": offering_id}
        }
        
        product_result = inventory.create_product(product_data)
        product_id = product_result.get('id')
        print(f"Created product subscription: {product_id}")
        

        # Step 4: Top up balance
        print("\n4. Balance Top-Up")
        print("-" * 20)
        balance_result = balance.create_adjustment(
            product_id=product_id,
            amount=1000,  # $10.00 in cents
            units="cents",
            description="Example balance top-up"
        )
        print(f"Created balance adjustment")

        # Step 5: Check balance buckets
        print("\n5. Balance Information")
        print("-" * 25)
        buckets = balance.list_buckets(product_id)
        if buckets:
            print(f"Found {len(buckets)} balance buckets:")
            for bucket in buckets:
                remaining_amount = bucket.get('remaining_amount', 'N/A')
                units = bucket.get('units', 'N/A')
                if remaining_amount != 'N/A' and units != 'N/A':
                    formatted_amount = balance.format_balance_amount(remaining_amount, units)
                    print(f"  - Bucket {bucket.get('id', 'N/A')}: {formatted_amount}")
                else:
                    print(f"  - Bucket {bucket.get('id', 'N/A')}: {remaining_amount} {units}")
        else:
            print("No balance buckets found")
        
        # Cleanup: Delete created entities
        print("\n6. Cleanup")
        print("-" * 15)
        try:
            print("Deleting created product subscription...")
            inventory.delete_product(product_id)
            print("Product subscription deleted")
            
            print("Deleting created service/subscriber...")
            service_inventory.delete_service(service_id)
            print("Service/subscriber deleted")
            
            print("Cleanup completed successfully!")
        except Exception as e:
            print(f"Cleanup failed: {e}")
            print("You may need to manually delete the created entities from the OCS web interface")

        print("\nCore operations completed successfully!")
        print("\nSummary:")
        print(f"  - Service ID: {service_id} (deleted)")
        print(f"  - Product ID: {product_id} (deleted)")
        print(f"  - Offering ID: {offering_id} (existing, not deleted)")
        
        print("\nNext steps:")
        print("- Check the OCS web interface to verify entities were deleted")
        print("- Run the example again to test the complete flow")
        print("- Use the API for your own SIM card management needs")
        

    except Exception as e:
        print(f"❌ Error during operations: {e}")
        print("This might be due to:")
        print("- Invalid credentials")
        print("- Network connectivity issues")
        print("- OCS API server not running")
        print("- Missing permissions")
    finally:
        client.close()
        print("\nConnection closed")

if __name__ == "__main__":
    main()
