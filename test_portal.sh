#!/bin/bash
echo "🔍 FORGE MEDIAS PORTAL TEST"
echo "==========================="

# Get IPs
EC2_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "Public IP: $EC2_IP"

# Test Docker
echo ""
echo "1. DOCKER STATUS:"
sudo docker ps

# Test local access
echo ""
echo "2. LOCAL ACCESS:"
curl -s http://localhost/api/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8000/api/health | python3 -m json.tool 2>/dev/null || echo "Local access failed"

# Check security group
echo ""
echo "3. SECURITY GROUP:"
SG_ID=$(aws ec2 describe-instances --instance-ids i-0a2b6598aa673452c --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' --output text)
aws ec2 describe-security-groups --group-ids $SG_ID --query 'SecurityGroups[0].IpPermissions[?FromPort==`80` || FromPort==`8000`].{Port:FromPort, Source:IpRanges[0].CidrIp}' --output table

# Final URLs
echo ""
echo "🎯 TEST URLs:"
echo "   Port 80:  http://$EC2_IP/"
echo "   Port 8000: http://$EC2_IP:8000/"
echo ""
echo "💡 Try both URLs in your browser!"
