# conftest.py
import pytest
from datetime import datetime

from utils.wechat_notify import send_wechat_message


def pytest_configure(config):
    config._test_results = {
        'start_time': datetime.now(),
        'total': 0,
        'passed': 0,
        'failed': 0,
        'failed_cases': []
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call':
        item.config._test_results['total'] += 1
        if report.failed:
            item.config._test_results['failed'] += 1
            item.config._test_results['failed_cases'].append({
                'name': report.nodeid,
                'error': str(report.longrepr)
            })
        elif report.passed:
            item.config._test_results['passed'] += 1


@pytest.fixture(scope="session", autouse=True)
def send_report(request):
    yield
    # 测试结束后执行推送
    results = request.config._test_results
    results['end_time'] = datetime.now()
    # 调用企业微信推送函数
    send_wechat_message(results)
