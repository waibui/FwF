import aiohttp
import asyncio
import argparse
from colorama import Fore, init
import time
from urllib.parse import urljoin
import os

# Initialize colorama for cross-platform colored output
init()

async def scan_url(session, base_url, path, timeout=10, allow_redirects=True):
    """Scan a single URL path and return the result."""
    url = urljoin(base_url, path.strip())
    try:
        start_time = time.time()
        async with session.get(url, timeout=timeout, allow_redirects=True) as response:
            elapsed = time.time() - start_time
            
            # Get the final URL after redirects
            final_url = str(response.url)
            
            # For redirects, note both the status code and the final URL
            redirect_info = ""
            if allow_redirects and final_url != url:
                redirect_info = f" -> {final_url}"
            
            return {
                'url': url,
                'final_url': final_url,
                'status': response.status,
                'elapsed': elapsed,
                'content_length': len(await response.read()),
                'redirect_info': redirect_info
            }
    except asyncio.TimeoutError:
        return {'url': url, 'final_url': url, 'status': 'TIMEOUT', 'elapsed': timeout, 'content_length': 0, 'redirect_info': ""}
    except Exception as e:
        return {'url': url, 'final_url': url, 'status': f'ERROR: {str(e)}', 'elapsed': 0, 'content_length': 0, 'redirect_info': ""}

async def scan_paths(base_url, wordlist_file, concurrent_tasks=100, timeout=10, allow_redirects=True):
    """Scan multiple paths concurrently from a wordlist file."""
    try:
        with open(wordlist_file, 'r') as f:
            paths = f.readlines()
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Could not read wordlist file: {e}{Fore.RESET}")
        return []

    print(f"{Fore.YELLOW}[INFO] Loaded {len(paths)} paths from {wordlist_file}{Fore.RESET}")
    print(f"{Fore.YELLOW}[INFO] Starting scan with {concurrent_tasks} concurrent requests{Fore.RESET}")
    print(f"{Fore.YELLOW}[INFO] Redirects: {'Enabled' if allow_redirects else 'Disabled'}{Fore.RESET}")
    
    results = []
    connector = aiohttp.TCPConnector(limit=concurrent_tasks, ssl=False)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Create a semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(concurrent_tasks)
        
        async def bounded_scan(path):
            async with semaphore:
                return await scan_url(session, base_url, path, timeout, allow_redirects)
        
        # Create tasks for all paths
        tasks = [bounded_scan(path) for path in paths]
        
        # Process results as they complete
        for i, future in enumerate(asyncio.as_completed(tasks), 1):
            result = await future
            results.append(result)
            
            # Determine color based on status code
            if isinstance(result['status'], int):
                if 200 <= result['status'] < 300:
                    color = Fore.GREEN
                elif 300 <= result['status'] < 400:
                    color = Fore.BLUE
                elif 400 <= result['status'] < 500:
                    color = Fore.YELLOW
                else:
                    color = Fore.RED
            else:
                color = Fore.RED
            
            # Print progress
            print(f"\r{Fore.CYAN}[PROGRESS] {i}/{len(paths)} paths scanned ({i/len(paths)*100:.1f}%){Fore.RESET}", end="")
            
            # Print interesting findings immediately
            if isinstance(result['status'], int) and result['status'] != 404:
                status_info = f"{result['status']}{result['redirect_info']}"
                print(f"\n{color}[FOUND] {status_info} - {result['url']} - {result['content_length']} bytes - {result['elapsed']:.2f}s{Fore.RESET}")
            elif not isinstance(result['status'], int):
                print(f"\n{color}[ERROR] {result['status']} - {result['url']}{Fore.RESET}")
    
    print(f"\n{Fore.GREEN}[COMPLETE] Scan finished!{Fore.RESET}")
    return results

def save_results(results, output_file):
    """Save scan results to a file."""
    try:
        with open(output_file, 'w') as f:
            f.write("URL,Final URL,Status,Content Length,Time(s)\n")
            for result in results:
                redirect_info = f",{result['final_url']}" if 'final_url' in result else ""
                f.write(f"{result['url']}{redirect_info},{result['status']},{result['content_length']},{result['elapsed']:.2f}\n")
        print(f"{Fore.GREEN}[SUCCESS] Results saved to {output_file}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Could not save results: {e}{Fore.RESET}")

def save_error_log(results, error_log_file):
    """Save detailed error information to a separate log file."""
    try:
        with open(error_log_file, 'w') as f:
            f.write("Error Type,URL,Details,Time(s)\n")
            for result in results:
                if not isinstance(result['status'], int):
                    error_type = "TIMEOUT" if result['status'] == "TIMEOUT" else "ERROR"
                    details = result['status']
                    f.write(f"{error_type},{result['url']},{details},{result['elapsed']:.2f}\n")
        print(f"{Fore.GREEN}[SUCCESS] Error log saved to {error_log_file}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR] Could not save error log: {e}{Fore.RESET}")

def main():
    parser = argparse.ArgumentParser(description='Fast Multi-threaded Web Path Scanner')
    parser.add_argument('-u', '--url', required=True, help='Base URL to scan (e.g., http://example.com/)')
    parser.add_argument('-w', '--wordlist', required=True, help='Path to wordlist file')
    parser.add_argument('-t', '--threads', type=int, default=50, help='Number of concurrent requests (default: 50)')
    parser.add_argument('-o', '--output', help='Output file for results (CSV format)')
    parser.add_argument('-e', '--error-log', help='Output file for error log (default: error_log.csv)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    parser.add_argument('-r', '--follow-redirects', action='store_true', help='Follow redirects (default: False)')
    args = parser.parse_args()
    
    # Set default error log filename if not provided
    if not args.error_log:
        args.error_log = "error_log.csv"
    
    print(f"{Fore.CYAN}=== Fast Multi-threaded Web Path Scanner ==={Fore.RESET}")
    
    # Run the async scanner
    start_time = time.time()
    results = asyncio.run(scan_paths(args.url, args.wordlist, args.threads, args.timeout, args.follow_redirects))
    total_time = time.time() - start_time
    
    # Display summary
    valid_results = [r for r in results if isinstance(r['status'], int)]
    success_count = sum(1 for r in valid_results if 200 <= r['status'] < 300)
    redirect_count = sum(1 for r in valid_results if 300 <= r['status'] < 400)
    client_error_count = sum(1 for r in valid_results if 400 <= r['status'] < 500)
    server_error_count = sum(1 for r in valid_results if 500 <= r['status'] < 600)
    
    # Count error types
    timeout_count = sum(1 for r in results if r['status'] == 'TIMEOUT')
    error_count = sum(1 for r in results if isinstance(r['status'], str) and r['status'].startswith('ERROR'))
    
    # Error details for console output
    if error_count > 0:
        print(f"\n{Fore.YELLOW}=== Error Details ==={Fore.RESET}")
        for result in results:
            if isinstance(result['status'], str) and result['status'].startswith('ERROR'):
                print(f"{Fore.RED}[ERROR] {result['url']} - {result['status']}{Fore.RESET}")
    
    print(f"\n{Fore.CYAN}=== Scan Summary ==={Fore.RESET}")
    print(f"Total paths scanned: {len(results)}")
    print(f"Successful (2xx): {success_count}")
    print(f"Redirects (3xx): {redirect_count}")
    print(f"Client Errors (4xx): {client_error_count}")
    print(f"Server Errors (5xx): {server_error_count}")
    print(f"Timeouts: {timeout_count}")
    print(f"Other errors: {error_count}")
    
    # Verification total
    http_total = success_count + redirect_count + client_error_count + server_error_count
    error_total = timeout_count + error_count
    print(f"HTTP responses: {http_total}")
    print(f"Error responses: {error_total}")
    print(f"Total responses: {http_total + error_total} (should match {len(results)})")
    
    print(f"Total scan time: {total_time:.2f} seconds")
    print(f"Average request time: {sum(r['elapsed'] for r in results)/len(results):.2f} seconds")
    
    # Save results if output file is specified
    if args.output:
        save_results(results, args.output)
        
    # Save error log if there are any errors
    if timeout_count > 0 or error_count > 0:
        save_error_log(results, args.error_log)
        print(f"{Fore.YELLOW}[INFO] Found {timeout_count + error_count} errors/timeouts. Details saved to {args.error_log}{Fore.RESET}")
    else:
        print(f"{Fore.GREEN}[INFO] No errors or timeouts detected.{Fore.RESET}")

if __name__ == "__main__":
    main()