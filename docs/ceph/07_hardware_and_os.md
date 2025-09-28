# Hardware and OS

- **CPU:** Multi-core processors recommended for better performance.
- **Memory:** Minimum 2 GB RAM per OSD; more is recommended for metadata servers (MDS).
- **Storage:** SSDs for journals/WAL/DB improve performance; HDDs for bulk storage.
- **Network:** 1 Gbps minimum; 10 Gbps or higher recommended for production.

## Supported Operating Systems

- **Linux:** Ceph is primarily developed for Linux distributions.
    - **Recommended:** Ubuntu 20.04/22.04 LTS, CentOS 7/8, RHEL 7/8, Debian 10/11.
- **Kernel:** Linux kernel 4.x or newer is recommended for optimal compatibility.

## Additional Recommendations

- Use enterprise-grade hardware for production clusters.
- Ensure all nodes have synchronized clocks (e.g., via NTP).
- Separate public and cluster networks for improved security and performance.
- Regularly update OS and Ceph packages for security and stability.
