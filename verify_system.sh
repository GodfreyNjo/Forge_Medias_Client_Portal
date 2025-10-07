#!/bin/bash
echo "🔍 FORGE MEDIAS SYSTEM VERIFICATION"
echo "==================================="

EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Public IP: $EC2_IP"

echo ""
echo "1. APPLICATION STATUS:"
curl -s http://localhost/api/health | python3 -m json.tool

echo ""
echo "2. AWS S3 BUCKET:"
aws s3 ls s3://forge-medias-uploads/ || echo "S3 bucket not accessible"

echo ""
echo "3. SERVICES AVAILABLE:"
curl -s http://localhost/api/services | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('Available services:')
for service in data['services']:
    print(f'  • {service['name']}')
    print(f'    Formats: {', '.join(service['supported_formats'])}')
"

echo ""
echo "4. DOCKER STATUS:"
sudo docker ps

echo ""
echo "🎯 TESTING INSTRUCTIONS:"
echo "   1. Open http://$EC2_IP/test in your browser"
echo "   2. Select a service and upload a test file"
echo "   3. Check if the order appears in the list"
echo "   4. Try downloading the file"
echo ""
echo "✅ System verification complete!"
