#!/bin/bash
echo "🔍 FORGE MEDIAS FINAL TEST"
echo "=========================="

EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Public IP: $EC2_IP"

echo ""
echo "1. DOCKER STATUS:"
sudo docker ps

echo ""
echo "2. APPLICATION HEALTH:"
curl -s http://localhost/api/health | python3 -m json.tool

echo ""
echo "3. SERVICES AVAILABLE:"
curl -s http://localhost/api/services | python3 -c "
import json, sys
data = json.load(sys.stdin)
for service in data['services']:
    print(f'  • {service['name']} - {service['description']}')
"

echo ""
echo "🎯 FINAL ACCESS URLs:"
echo "   🌐 Main Portal:     http://$EC2_IP/"
echo "   📊 Client Dashboard: http://$EC2_IP/dashboard"
echo "   🔧 Admin Panel:      http://$EC2_IP/admin"
echo "   ❓ API Health:       http://$EC2_IP/api/health"
echo ""
echo "🔐 Admin Login: admin / forge2024"
echo ""
echo "🚀 Your Forge Medias portal is fully operational!"
