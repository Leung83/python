#!/bin/bash

OCLD=$(sudo awk '/ocld/{print$2}' /etc/hosts)
CMP=$(sudo awk '/cmp/{print$2}' /etc/hosts | sort -t"p" -k2n,2)

# Save Overcloud RPM info in /tmp
for ocld in ${OCLD[@]}
do
       (ssh -q -oStrictHostKeyChecking=no -oConnectTimeout=5 ${ocld} rpm -qa | egrep "^haproxy|^httpd|^kernel|^libvirt|^mongodb|^ntp|^openstack|^puppet|^python|^gdb|^qemu" | sort > /tmp/${ocld}_rpm.txt)&
done
wait

# Diff RPM info and save to test result files
echo "======================= OCLD1 vs OCLD2 =======================" > /tmp/rpm_result.txt
RES=$(diff -y --suppress-common-lines /tmp/ocld1_rpm.txt /tmp/ocld2_rpm.txt)

if [ "$RES" != "" ]
then
        echo -e "[NOK]\n$RES" >> /tmp/rpm_result.txt
else
        echo -e "[OK]" >> /tmp/rpm_result.txt
fi


echo -e "\n======================= OCLD2 vs OCLD3 =======================" >> /tmp/rpm_result.txt
RES=$(diff -y --suppress-common-lines /tmp/ocld2_rpm.txt /tmp/ocld3_rpm.txt )

if [ "$RES" != "" ]
then
        echo -e "[NOK]\n$RES" >> /tmp/rpm_result.txt
else
        echo -e "[OK]" >> /tmp/rpm_result.txt
fi


# Save Compute RPM info in /tmp
for cmp in ${CMP[@]}
do
        (ssh -q -oStrictHostKeyChecking=no -oConnectTimeout=5 ${cmp} rpm -qa | egrep "^ca-cert|^kernel|^libvirt|multipath|^ntp|^openstack|^puppet|^python|^gdb|^qemu" | sort > /tmp/${cmp}_rpm.txt)&
done
wait

# Diff RPM info and save to test result files
for cmp in ${CMP[@]}
do
        echo -e "\n======================= cmp1 vs $cmp =======================" >> /tmp/rpm_result.txt
        RES=$(diff -y --suppress-common-lines /tmp/cmp1_rpm.txt /tmp/${cmp}_rpm.txt)

        if [ "$RES" != "" ]
        then
                echo -e "[NOK]\n$RES" >> /tmp/rpm_result.txt
        else
                echo -e "[OK]" >> /tmp/rpm_result.txt
        fi
done

echo "Done!"
