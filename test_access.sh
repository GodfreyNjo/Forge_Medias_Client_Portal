#!/bin/bash
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "🔍 Testing Forge Medias Portal Access..."
echo "Public IP: $EC2_IP"
echo ""

# Test basic connectivity
echo "1. Testing API health..."
curl -s http://$EC2_IP:8000/api/health && echo " ✅ API Healthy" || echo " ❌ API Failed"

echo ""
echo "2. Testing admin access..."
curl -s -u admin:forge2024 http://$EC2_IP:8000/api/admin/jobs > /dev/null && echo " ✅ Admin Access Working" || echo " ❌ Admin Access Failed"

echo ""
echo "🎊 ACCESS URLs:"
echo "   Client Portal: http://$EC2_IP:8000/"
echo "   Admin Panel:   http://$EC2_IP:8000/admin"
echo "   API Health:    http://$EC2_IP:8000/api/health"
